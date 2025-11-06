"""Content creation crew for generating personalized attendee content."""

from pathlib import Path
from typing import Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from event_style_scraper.types import EventStyleConfig


@CrewBase
class ContentCreationCrew:
    """
    Content creation crew for generating brand-aligned personalized content.

    This crew uses 4 specialized agents to create engaging, personalized
    content for event attendees that matches the event's brand voice.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, attendee_data: Dict[str, Any], style_config: EventStyleConfig):
        """
        Initialize ContentCreationCrew.

        Args:
            attendee_data: Dictionary containing attendee information
            style_config: EventStyleConfig with brand voice settings
        """
        self.attendee_data = attendee_data
        self.style_config = style_config

        # Get config directory path
        self.config_dir = Path(__file__).parent / "config"

    @agent
    def content_writer_agent(self) -> Agent:
        """Create content writer agent."""
        return Agent(
            config=self.agents_config["content_writer_agent"],
            verbose=True
        )

    @agent
    def personalization_agent(self) -> Agent:
        """Create personalization specialist agent."""
        return Agent(
            config=self.agents_config["personalization_agent"],
            verbose=True
        )

    @agent
    def brand_voice_agent(self) -> Agent:
        """Create brand voice guardian agent."""
        return Agent(
            config=self.agents_config["brand_voice_agent"],
            verbose=True
        )

    @agent
    def quality_editor_agent(self) -> Agent:
        """Create quality editor agent."""
        return Agent(
            config=self.agents_config["quality_editor_agent"],
            verbose=True
        )

    @task
    def analyze_attendee(self) -> Task:
        """Create task to analyze attendee experience."""
        # Extract attendee info for task description interpolation
        attendee_name = f"{self.attendee_data.get('firstName', '')} {self.attendee_data.get('lastName', '')}".strip()
        session_count = len(self.attendee_data.get('sessions', []))
        connection_count = len(self.attendee_data.get('connections', []))

        task_config = self.tasks_config["analyze_attendee"].copy()

        # Interpolate variables in description
        task_config["description"] = task_config["description"].format(
            attendee_name=attendee_name,
            session_count=session_count,
            connection_count=connection_count
        )

        return Task(
            config=task_config,
            agent=self.personalization_agent()
        )

    @task
    def generate_content(self) -> Task:
        """Create task to generate personalized content."""
        return Task(
            config=self.tasks_config["generate_content"],
            agent=self.content_writer_agent()
        )

    @task
    def apply_brand_voice(self) -> Task:
        """Create task to apply brand voice to content."""
        task_config = self.tasks_config["apply_brand_voice"].copy()

        # Interpolate brand voice variables in description
        task_config["description"] = task_config["description"].format(
            brand_tone=self.style_config.brand_voice.tone,
            brand_style=self.style_config.brand_voice.style,
            brand_keywords=", ".join(self.style_config.brand_voice.keywords)
        )

        return Task(
            config=task_config,
            agent=self.brand_voice_agent()
        )

    @task
    def quality_check(self) -> Task:
        """Create task to perform quality check on content."""
        return Task(
            config=self.tasks_config["quality_check"],
            agent=self.quality_editor_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Create the content creation crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
