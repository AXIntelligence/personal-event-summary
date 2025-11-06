"""Pydantic data models for event style configuration."""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class ColorPalette(BaseModel):
    """Color palette configuration for an event."""

    primary: str = Field(..., description="Primary brand color")
    secondary: str = Field(..., description="Secondary brand color")
    accent: str = Field(..., description="Accent color for highlights")
    background: str = Field(..., description="Background color")
    text: str = Field(..., description="Text color")

    @field_validator("primary", "secondary", "accent", "background", "text")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Validate color is in valid CSS format."""
        # Accept hex format (#RGB, #RRGGBB, #RRGGBBAA)
        hex_pattern = r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$"
        # Accept rgb/rgba format
        rgb_pattern = r"^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*[\d.]+\s*)?\)$"
        # Accept hsl/hsla format
        hsl_pattern = r"^hsla?\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*(,\s*[\d.]+\s*)?\)$"

        if not (
            re.match(hex_pattern, v)
            or re.match(rgb_pattern, v)
            or re.match(hsl_pattern, v)
        ):
            raise ValueError(
                f"Invalid color format: {v}. Must be hex (#RGB), rgb(r,g,b), or hsl(h,s,l)"
            )
        return v


class Typography(BaseModel):
    """Typography configuration for an event."""

    heading_font: str = Field(..., description="Font family for headings")
    body_font: str = Field(..., description="Font family for body text")
    heading_size: str = Field(default="2rem", description="Base heading font size")
    body_size: str = Field(default="1rem", description="Base body font size")
    line_height: str = Field(default="1.6", description="Line height multiplier")


class BrandVoice(BaseModel):
    """Brand voice and tone configuration for an event."""

    tone: str = Field(..., description="Overall tone (professional, casual, energetic, etc.)")
    keywords: list[str] = Field(
        default_factory=list, description="Key brand keywords and phrases"
    )
    style: str = Field(..., description="Writing style (formal, conversational, technical, etc.)")
    personality: Optional[str] = Field(
        default=None, description="Brand personality descriptor"
    )


class LayoutConfig(BaseModel):
    """Layout and spacing configuration for an event."""

    grid_system: str = Field(
        default="flexbox", description="Grid system (flexbox, grid, 12-column)"
    )
    spacing_unit: str = Field(default="8px", description="Base spacing unit")
    border_radius: str = Field(default="8px", description="Default border radius")
    container_width: str = Field(default="1200px", description="Max container width")


class EventStyleConfig(BaseModel):
    """Complete style configuration for an event."""

    event_id: str = Field(..., description="Unique event identifier")
    event_name: str = Field(..., description="Event display name")
    source_url: str = Field(..., description="Source website URL")
    colors: ColorPalette = Field(..., description="Color palette")
    typography: Typography = Field(..., description="Typography settings")
    brand_voice: BrandVoice = Field(..., description="Brand voice and tone")
    layout: Optional[LayoutConfig] = Field(
        default_factory=LayoutConfig, description="Layout configuration"
    )
    logo_url: Optional[str] = Field(default=None, description="Logo image URL")
    favicon_url: Optional[str] = Field(default=None, description="Favicon URL")
    scraped_at: Optional[str] = Field(default=None, description="Timestamp of scraping")

    model_config = {"extra": "forbid"}  # Prevent extra fields
