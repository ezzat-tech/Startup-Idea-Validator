from pydantic import BaseModel, Field
from typing import List

class Competitor(BaseModel):
    name: str = Field(description="Name of the competitor")
    description: str = Field(description="Short description of what they do")
    pricing: str = Field(description="Estimated pricing or business model")
    strengths: List[str] = Field(description="What are they doing well?")
    weaknesses: List[str] = Field(description="Where are they failing or missing features")

class MarketGap(BaseModel):
    title: str = Field(description="Brief title of the gap in the market")
    description: str = Field(description="Detailed explanation of why this is an opportunity")
    evidence: str = Field(description="Quotes or data from search results that prove this gap exists")

class VentureReport(BaseModel):
    startup_name: str = Field(description="The name of the proposed startup")
    summary: str = Field(description="A high-level overview of the market landscape")
    competitors: List[Competitor] = Field(description="List of top 3-5 competitors")
    market_gaps: List[MarketGap] = Field(description="Opportunities identified during research")
    final_recommendation: str = Field(description="Should the founder proceed? Pivot? How to win?")

class Critique(BaseModel):
    """Structured feedback from the Critic agent."""
    has_issues: bool = Field(description="True if the report needs improvement")
    missing_competitor_info: List[str] = Field(
        description="List of competitors that are missing pricing, strengths, or weaknesses"
    )
    vague_market_gaps: List[str] = Field(
        description="List of market gap titles that lack concrete evidence"
    )
    actionable_feedback: str = Field(
        description="Specific instructions for the Researcher to improve the report"
    )