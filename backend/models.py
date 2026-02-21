from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ManagementTone(str, Enum):
    optimistic = "optimistic"
    neutral = "neutral"
    cautious = "cautious"
    pessimistic = "pessimistic"
    not_mentioned = "Not mentioned in transcript"

class ConfidenceLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    not_mentioned = "Not mentioned in transcript"

class ForwardGuidance(BaseModel):
    revenue: str = Field(description="Forward guidance regarding revenue. If missing, output 'Not mentioned in transcript'")
    margin: str = Field(description="Forward guidance regarding margins. If missing, output 'Not mentioned in transcript'")
    capex: str = Field(description="Forward guidance regarding capital expenditures (capex). If missing, output 'Not mentioned in transcript'")

class EarningsCallSummary(BaseModel):
    management_tone: ManagementTone = Field(description="Overall tone of the management.")
    confidence_level: ConfidenceLevel = Field(description="Level of confidence expressed by management.")
    key_positives: List[str] = Field(description="3-5 key positive points mentioned.", min_length=1)
    key_concerns: List[str] = Field(description="3-5 key concerns or risks mentioned.", min_length=1)
    forward_guidance: ForwardGuidance = Field(description="Forward guidance details.")
    capacity_utilization: str = Field(description="Information regarding capacity utilization. If missing, output 'Not mentioned in transcript'")
    growth_initiatives: List[str] = Field(description="2-3 specific growth initiatives mentioned.", min_length=1)
    limitations: List[str] = Field(description="Limitations, headwinds or challenges discussed.", min_length=1)
