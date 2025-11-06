"""StyleExtractionCrew - Multi-agent crew for web scraping and style extraction."""

import os
from pathlib import Path
from typing import Any, Dict, List
import yaml

from crewai import Agent, Crew, Task, Process
from dotenv import load_dotenv

from event_style_scraper.tools import WebScraperTool


# Load environment variables
load_dotenv()


class StyleExtractionCrew:
    """
    Multi-agent crew for extracting styles and brand voice from event websites.

    This crew orchestrates 4 agents:
    1. WebScraperAgent: Scrapes HTML/CSS using Playwright
    2. StyleAnalystAgent: Extracts colors, typography, layout
    3. VoiceAnalystAgent: Identifies brand voice and tone
    4. CompilerAgent: Compiles results into EventStyleConfig JSON
    """

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
        from event_style_scraper.tools import SecurityError
        scraper_tool = WebScraperTool(timeout=timeout)
        try:
            scraper_tool.validate_url(url)
        except SecurityError as e:
            raise ValueError(str(e)) from e

        # Load configurations
        self.config_dir = Path(__file__).parent / "config"
        self.agents_config = self._load_yaml(self.config_dir / "agents.yaml")
        self.tasks_config = self._load_yaml(self.config_dir / "tasks.yaml")

    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML configuration file."""
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def agents(self) -> List[Agent]:
        """Create and return all agents for the crew."""
        agents_list = []

        # Web Scraper Agent
        web_scraper = Agent(
            role=self.agents_config["web_scraper_agent"]["role"].strip(),
            goal=self.agents_config["web_scraper_agent"]["goal"].strip(),
            backstory=self.agents_config["web_scraper_agent"]["backstory"].strip(),
            verbose=True,
            allow_delegation=False,
        )
        agents_list.append(web_scraper)

        # Style Analyst Agent
        style_analyst = Agent(
            role=self.agents_config["style_analyst_agent"]["role"].strip(),
            goal=self.agents_config["style_analyst_agent"]["goal"].strip(),
            backstory=self.agents_config["style_analyst_agent"]["backstory"].strip(),
            verbose=True,
            allow_delegation=False,
        )
        agents_list.append(style_analyst)

        # Voice Analyst Agent
        voice_analyst = Agent(
            role=self.agents_config["voice_analyst_agent"]["role"].strip(),
            goal=self.agents_config["voice_analyst_agent"]["goal"].strip(),
            backstory=self.agents_config["voice_analyst_agent"]["backstory"].strip(),
            verbose=True,
            allow_delegation=False,
        )
        agents_list.append(voice_analyst)

        # Compiler Agent
        compiler = Agent(
            role=self.agents_config["compiler_agent"]["role"].strip(),
            goal=self.agents_config["compiler_agent"]["goal"].strip(),
            backstory=self.agents_config["compiler_agent"]["backstory"].strip(),
            verbose=True,
            allow_delegation=False,
        )
        agents_list.append(compiler)

        return agents_list

    def tasks(self) -> List[Task]:
        """Create and return all tasks for the crew."""
        agents = self.agents()
        tasks_list = []

        # Task 1: Scrape Website
        scrape_task = Task(
            description=self.tasks_config["scrape_website"]["description"].format(url=self.url),
            expected_output=self.tasks_config["scrape_website"]["expected_output"],
            agent=agents[0],  # web_scraper_agent
        )
        tasks_list.append(scrape_task)

        # Task 2: Extract Styles
        extract_styles_task = Task(
            description=self.tasks_config["extract_styles"]["description"],
            expected_output=self.tasks_config["extract_styles"]["expected_output"],
            agent=agents[1],  # style_analyst_agent
            context=[scrape_task],
        )
        tasks_list.append(extract_styles_task)

        # Task 3: Analyze Voice
        analyze_voice_task = Task(
            description=self.tasks_config["analyze_voice"]["description"],
            expected_output=self.tasks_config["analyze_voice"]["expected_output"],
            agent=agents[2],  # voice_analyst_agent
            context=[scrape_task],
        )
        tasks_list.append(analyze_voice_task)

        # Task 4: Compile Config
        compile_task = Task(
            description=self.tasks_config["compile_config"]["description"],
            expected_output=self.tasks_config["compile_config"]["expected_output"],
            agent=agents[3],  # compiler_agent
            context=[scrape_task, extract_styles_task, analyze_voice_task],
        )
        tasks_list.append(compile_task)

        return tasks_list

    def crew(self) -> Crew:
        """Create and return the configured crew."""
        return Crew(
            agents=self.agents(),
            tasks=self.tasks(),
            process=Process.sequential,
            verbose=True,
        )

    def kickoff(self) -> Any:
        """Execute the crew and return results."""
        crew = self.crew()
        return crew.kickoff()
