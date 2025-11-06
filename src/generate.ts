/**
 * Page Generation Module
 *
 * Generates personalized HTML pages for event attendees using Handlebars templates.
 * Includes batch generation and static asset copying.
 */

import { readFile, writeFile, mkdir, cp } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import Handlebars from 'handlebars';
import { loadEvent, loadAttendee, loadAllAttendees, loadStyleConfig } from './dataLoader.js';
import { generateEventCSS } from './cssGenerator.js';
import type { Event, Attendee } from './types/index.js';

// Get directory name for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Paths
const TEMPLATES_DIR = join(__dirname, '..', 'templates');
const STATIC_DIR = join(__dirname, '..', 'static');
const DEFAULT_DIST_DIR = join(__dirname, '..', 'dist');

/**
 * Sets up Handlebars with templates, partials, and helpers
 *
 * @returns Configured Handlebars instance
 */
export async function setupHandlebars(): Promise<typeof Handlebars> {
  const hbs = Handlebars.create();

  // Register helpers
  hbs.registerHelper('formatDate', (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  });

  hbs.registerHelper('substring', (str: string, start: number, end: number) => {
    if (!str) return '';
    return str.substring(start, end);
  });

  hbs.registerHelper('currentYear', () => {
    return new Date().getFullYear();
  });

  // Register partials
  const ctaPartialPath = join(TEMPLATES_DIR, 'partials', 'cta.hbs');
  const ctaPartial = await readFile(ctaPartialPath, 'utf-8');
  hbs.registerPartial('cta', ctaPartial);

  const productsPartialPath = join(TEMPLATES_DIR, 'partials', 'products.hbs');
  const productsPartial = await readFile(productsPartialPath, 'utf-8');
  hbs.registerPartial('products', productsPartial);

  const boothsPartialPath = join(TEMPLATES_DIR, 'partials', 'booths.hbs');
  const boothsPartial = await readFile(boothsPartialPath, 'utf-8');
  hbs.registerPartial('booths', boothsPartial);

  return hbs;
}

/**
 * Compiles the base layout and attendee page templates
 *
 * @param hbs Handlebars instance
 * @returns Object with compiled templates
 */
async function compileTemplates(hbs: typeof Handlebars) {
  const baseLayoutPath = join(TEMPLATES_DIR, 'layouts', 'base.hbs');
  const attendeePagePath = join(TEMPLATES_DIR, 'pages', 'attendee.hbs');

  const baseLayout = await readFile(baseLayoutPath, 'utf-8');
  const attendeePage = await readFile(attendeePagePath, 'utf-8');

  // Compile attendee page content
  const attendeeTemplate = hbs.compile(attendeePage);

  // Create a function that renders content into base layout
  const render = async (attendee: Attendee, event: Event) => {
    // Load style config if available (Plan 003)
    const styleConfig = await loadStyleConfig(event.id);
    const eventCSS = styleConfig ? generateEventCSS(styleConfig) : null;

    // First render the attendee page content
    const pageContent = attendeeTemplate({ attendee, event });

    // Then render the full page with layout
    const fullPageTemplate = hbs.compile(baseLayout);
    return fullPageTemplate({
      body: pageContent,
      attendee,
      event,
      eventCSS,
      pageTitle: `${attendee.firstName} ${attendee.lastName} - ${event.name}`,
      description: `${attendee.firstName}'s personalized ${event.name} experience summary`
    });
  };

  return { render };
}

/**
 * Generates an HTML page for a single attendee
 *
 * @param attendeeId Attendee identifier
 * @param distDir Output directory (default: dist/)
 * @returns Path to generated file
 */
export async function generateAttendeePage(
  attendeeId: string,
  distDir: string = DEFAULT_DIST_DIR
): Promise<string> {
  try {
    // Load data
    const attendee = await loadAttendee(attendeeId);
    const event = await loadEvent(attendee.eventId);

    // Setup Handlebars
    const hbs = await setupHandlebars();
    const { render } = await compileTemplates(hbs);

    // Render HTML (now async due to style config loading)
    const html = await render(attendee, event);

    // Create output directory
    const outputDir = join(distDir, 'attendees', attendeeId);
    await mkdir(outputDir, { recursive: true });

    // Write file
    const outputPath = join(outputDir, 'index.html');
    await writeFile(outputPath, html, 'utf-8');

    return outputPath;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to generate page for attendee ${attendeeId}: ${error.message}`);
    }
    throw new Error(`Failed to generate page for attendee ${attendeeId}`);
  }
}

/**
 * Generates HTML pages for all attendees
 *
 * @param distDir Output directory (default: dist/)
 * @returns Array of paths to generated files
 */
export async function generateAllAttendeePages(
  distDir: string = DEFAULT_DIST_DIR
): Promise<string[]> {
  try {
    // Load all attendees
    const attendees = await loadAllAttendees();

    if (attendees.length === 0) {
      console.warn('No attendees found to generate pages for');
      return [];
    }

    console.log(`Generating pages for ${attendees.length} attendees...`);

    // Setup Handlebars once for all attendees (more efficient)
    const hbs = await setupHandlebars();

    // Load event data (assuming all attendees are for same event)
    const event = await loadEvent(attendees[0].eventId);

    // Compile templates once
    const { render } = await compileTemplates(hbs);

    // Generate all pages in parallel
    const generationPromises = attendees.map(async (attendee) => {
      try {
        // Render HTML (now async due to style config loading)
        const html = await render(attendee, event);

        // Create output directory
        const outputDir = join(distDir, 'attendees', attendee.id);
        await mkdir(outputDir, { recursive: true });

        // Write file
        const outputPath = join(outputDir, 'index.html');
        await writeFile(outputPath, html, 'utf-8');

        return outputPath;
      } catch (error) {
        console.error(`Error generating page for attendee ${attendee.id}:`, error);
        throw error;
      }
    });

    const results = await Promise.all(generationPromises);

    console.log(`✓ Generated ${results.length} attendee pages`);

    return results;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to generate attendee pages: ${error.message}`);
    }
    throw new Error('Failed to generate attendee pages');
  }
}

/**
 * Copies static assets (CSS, images) to dist directory
 *
 * @param distDir Output directory (default: dist/)
 */
export async function copyStaticAssets(
  distDir: string = DEFAULT_DIST_DIR
): Promise<void> {
  try {
    const staticDistDir = join(distDir, 'static');

    // Create static directory
    await mkdir(staticDistDir, { recursive: true });

    // Copy entire static directory
    await cp(STATIC_DIR, staticDistDir, { recursive: true, force: true });

    console.log('✓ Copied static assets');
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to copy static assets: ${error.message}`);
    }
    throw new Error('Failed to copy static assets');
  }
}

/**
 * Main generation function - generates all pages and copies assets
 *
 * @param distDir Output directory (default: dist/)
 */
export async function generateAll(distDir: string = DEFAULT_DIST_DIR): Promise<void> {
  try {
    console.log('Starting page generation...\n');

    // Generate all attendee pages
    const pages = await generateAllAttendeePages(distDir);

    // Copy static assets
    await copyStaticAssets(distDir);

    console.log(`\n✅ Generation complete!`);
    console.log(`   Pages generated: ${pages.length}`);
    console.log(`   Output directory: ${distDir}`);
  } catch (error) {
    console.error('\n❌ Generation failed:', error);
    throw error;
  }
}

// CLI execution
if (import.meta.url === `file://${process.argv[1]}`) {
  generateAll()
    .then(() => {
      process.exit(0);
    })
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}
