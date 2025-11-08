# GitHub Actions Debug Logging

## Methods to Enable Debug Logging

### 1. Application-Level Debug (Already Enabled)

The workflow now includes debug environment variables and `--debug` flag:

```yaml
env:
  CI: true
  CREWAI_VERBOSE: "True"     # CrewAI verbosity
  OPENAI_LOG: "debug"        # OpenAI API debug logs
  LOG_LEVEL: "DEBUG"         # Python logging level
  HTTPX_LOG_LEVEL: "DEBUG"   # HTTP client debug logs
```

And the scrape command now uses `--debug`:
```bash
PYTHONPATH=./src python -m event_style_scraper scrape \
  --url "https://$event" \
  --timeout 90 \
  --debug
```

### 2. GitHub Actions Runner Debug Mode

Enable detailed runner diagnostics:

#### Option A: Repository Secrets (Permanent)

```bash
# Add repository secrets
gh secret set ACTIONS_RUNNER_DEBUG --body "true"
gh secret set ACTIONS_STEP_DEBUG --body "true"
```

#### Option B: Re-run with Debug (Per-run)

In GitHub UI:
1. Go to Actions tab
2. Click on a workflow run
3. Click "Re-run jobs" dropdown
4. Select "**Re-run jobs with debug logging**"

#### Option C: Environment Variables (One-time)

Not available for workflow_dispatch, but you could add to workflow file:

```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

### 3. View Logs in GitHub

After run completes:

```bash
# Download logs
gh run view <run-id> --log > workflow_debug.log

# Search for specific patterns
gh run view <run-id> --log | grep -i "openai"
gh run view <run-id> --log | grep -i "connection"
gh run view <run-id> --log | grep -i "error"

# Check timing (look for long gaps)
gh run view <run-id> --log | grep "⏰"
```

### 4. Real-time Monitoring

```bash
# Watch workflow as it runs
gh run watch <run-id>

# Or manually check every few minutes
gh run view <run-id> --log | tail -100
```

## What Each Debug Mode Shows

### Application Debug (`--debug` flag)
**Shows:**
- Timestamp for every log line
- HTTP request/response details
- OpenAI API calls (request body, response)
- Network connection attempts
- Token usage per API call
- CrewAI agent thoughts and actions

**Example Output:**
```
2025-11-08 03:35:45 - httpx - DEBUG - Sending request: POST https://api.openai.com/v1/chat/completions
2025-11-08 03:35:45 - httpx - DEBUG - Request headers: {...}
2025-11-08 03:35:45 - openai - DEBUG - Request body: {...}
[... silence indicates hanging ...]
2025-11-08 03:48:45 - httpx - ERROR - Connection timeout after 780s
```

### Runner Debug (`ACTIONS_RUNNER_DEBUG`)
**Shows:**
- Internal runner state
- Environment variable setup
- Process spawning
- File system operations
- Step execution details

**Use when:** Debugging workflow structure issues, not application issues.

### Step Debug (`ACTIONS_STEP_DEBUG`)
**Shows:**
- Variable expansion
- Command substitution
- Shell execution details
- Exit codes

**Use when:** Debugging bash script issues in workflow steps.

## Interpreting Debug Output

### Normal Successful Run

```
================================================
🌐 Scraping: eventtechlive.com
⏰ Start time: 2025-11-08T03:35:44Z
================================================
2025-11-08 03:35:45 - httpx - DEBUG - Sending request to OpenAI
2025-11-08 03:35:46 - openai - INFO - Response received (200 OK)
2025-11-08 03:35:46 - httpx - DEBUG - Tokens used: 1234
✅ Style extraction completed!
⏰ End time: 2025-11-08T03:36:15Z
================================================
```
**Duration:** ~30 seconds ✅

### Hanging on OpenAI API

```
================================================
🌐 Scraping: eventtechlive.com
⏰ Start time: 2025-11-08T03:35:44Z
================================================
2025-11-08 03:35:45 - httpx - DEBUG - Sending request to OpenAI
[13 minutes of silence - NO logs]
2025-11-08 03:48:45 - httpx - ERROR - Connection timeout
⏰ End time: 2025-11-08T03:48:45Z
================================================
```
**Duration:** ~13 minutes ❌ **Network timeout issue**

### API Key Invalid

```
2025-11-08 03:35:45 - openai - ERROR - Authentication failed
2025-11-08 03:35:45 - openai - ERROR - Invalid API key provided
❌ Scraping failed: Invalid API key
```
**Duration:** < 1 second ❌ **API key problem**

### Rate Limited

```
2025-11-08 03:35:45 - openai - WARNING - Rate limit exceeded
2025-11-08 03:35:45 - openai - INFO - Retrying in 20 seconds...
2025-11-08 03:36:05 - httpx - DEBUG - Retry attempt 1
```
**Duration:** Variable ⚠️ **Rate limiting**

## Timing Analysis

### Calculate Scraping Duration

```bash
# Extract timing from logs
gh run view <run-id> --log | grep "⏰" | tee timing.txt

# Example output:
# ⏰ Start time: 2025-11-08T03:35:44Z
# ⏰ End time: 2025-11-08T03:48:45Z

# Calculate duration (manually or with script)
```

### Identify Long Gaps

```bash
# Show all logs with timestamps
gh run view <run-id> --log | grep -E "^\d{4}-\d{2}-\d{2}" > timed_logs.txt

# Look for large time gaps between consecutive lines
awk '{
  if (NR > 1) {
    gsub(/[:-]/, " ", $1" "$2)
    cmd = "date -d \"" $1" "$2 "\" +%s"
    cmd | getline current
    close(cmd)
    diff = current - prev
    if (diff > 60) {
      print "⚠️ GAP: " diff "s between " prev_line " and " $0
    }
  }
  prev = current
  prev_line = $0
}' timed_logs.txt
```

## Quick Debug Commands

```bash
# 1. Trigger new run with debug enabled
gh workflow run scrape-and-deploy.yml

# 2. Get run ID
RUN_ID=$(gh run list --limit 1 --json databaseId -q '.[0].databaseId')

# 3. Monitor in real-time
gh run watch $RUN_ID

# 4. Download logs when done
gh run view $RUN_ID --log > debug_output.log

# 5. Analyze timing
grep "⏰" debug_output.log

# 6. Check for errors
grep -i "error\|fail\|timeout" debug_output.log

# 7. Check OpenAI calls
grep -i "openai\|httpx" debug_output.log | head -50
```

## Troubleshooting Specific Issues

### Issue: No Debug Logs Appearing

**Cause:** Python logging not configured before imports.

**Fix:** Our CLI now configures logging at startup (✅ already fixed).

### Issue: Logs Cut Off Mid-Stream

**Cause:** GitHub Actions log size limit (500MB) or truncation.

**Fix:** Add `flush: true` to echo commands:
```bash
echo "Log message"
python -u script.py  # -u for unbuffered output
```

### Issue: Can't See HTTP Request Bodies

**Cause:** `HTTPX_LOG_LEVEL` not set.

**Fix:** Already set to `DEBUG` in workflow (✅ already enabled).

### Issue: Workflow Canceled Before Completion

**Cause:** Manual cancellation or timeout (max 360 minutes for free tier).

**Fix:** Increase timeout or optimize scraping:
```yaml
jobs:
  scrape:
    timeout-minutes: 30  # Add explicit timeout
```

## Best Practices

1. **Always check timing first** - Look at `⏰` markers to identify where delays occur
2. **Search for errors** - Use `grep -i error` to find failures quickly
3. **Check API key validity** - "Invalid API key" errors appear within 1 second
4. **Look for long silences** - Gaps >5 minutes = likely network timeout
5. **Compare timestamps** - Start vs End time should match expected duration

## Related Files

- `.github/workflows/scrape-and-deploy.yml` - Workflow with debug enabled
- `python/src/event_style_scraper/cli.py` - CLI with --debug flag
- `docs/enable-debug-logging.md` - Local debug setup
- `docs/troubleshooting-api-key.md` - API key troubleshooting
