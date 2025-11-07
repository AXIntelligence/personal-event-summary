"""StyleExtractionCrew - Multi-agent crew for web scraping and style extraction."""

from pathlib import Path
from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from event_style_scraper.tools import WebScraperTool, SecurityError, PlaywrightStyleExtractorTool


@CrewBase
class StyleExtractionCrew:
    """
    Multi-agent crew for extracting styles and brand voice from event websites.

    This crew orchestrates 4 agents:
    1. WebScraperAgent: Scrapes HTML/CSS using Playwright
    2. StyleAnalystAgent: Extracts colors, typography, layout
    3. VoiceAnalystAgent: Identifies brand voice and tone
    4. CompilerAgent: Compiles results into EventStyleConfig JSON
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, url: str, timeout: int = 60):
        """
        Initialize StyleExtractionCrew.

        Args:
            url: URL of the event website to scrape
            timeout: Maximum time in seconds for scraping operations
        """
        self.url = url
        self.timeout = timeout

        # Validate URL using security tool
        scraper_tool = WebScraperTool(timeout=timeout)
        try:
            scraper_tool.validate_url(url)
        except SecurityError as e:
            raise ValueError(str(e)) from e

        # Get config directory path
        self.config_dir = Path(__file__).parent / "config"

    @agent
    def web_scraper_agent(self) -> Agent:
        """Create web scraper agent with Playwright tool."""
        return Agent(
            config=self.agents_config["web_scraper_agent"],
            tools=[PlaywrightStyleExtractorTool(timeout=self.timeout * 1000)],  # Convert seconds to milliseconds
            verbose=True,
            allow_delegation=False
        )

    @agent
    def style_analyst_agent(self) -> Agent:
        """Create style analyst agent."""
        return Agent(
            config=self.agents_config["style_analyst_agent"],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def voice_analyst_agent(self) -> Agent:
        """Create voice analyst agent."""
        return Agent(
            config=self.agents_config["voice_analyst_agent"],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def compiler_agent(self) -> Agent:
        """Create compiler agent."""
        return Agent(
            config=self.agents_config["compiler_agent"],
            verbose=True,
            allow_delegation=False
        )

    @task
    def scrape_website(self) -> Task:
        """Create task to scrape website."""
        task_config = self.tasks_config["scrape_website"].copy()
        task_config["description"] = task_config["description"].format(url=self.url)

        return Task(
            config=task_config,
            agent=self.web_scraper_agent()
        )

    @task
    def extract_styles(self) -> Task:
        """Create task to extract styles."""
        return Task(
            config=self.tasks_config["extract_styles"],
            agent=self.style_analyst_agent()
        )

    @task
    def analyze_voice(self) -> Task:
        """Create task to analyze brand voice."""
        return Task(
            config=self.tasks_config["analyze_voice"],
            agent=self.voice_analyst_agent()
        )

    @task
    def compile_config(self) -> Task:
        """Create task to compile configuration."""
        from event_style_scraper.types import EventStyleConfig

        return Task(
            config=self.tasks_config["compile_config"],
            agent=self.compiler_agent(),
            output_pydantic=EventStyleConfig  # Native Pydantic output
        )

    @crew
    def crew(self) -> Crew:
        """Create the style extraction crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
