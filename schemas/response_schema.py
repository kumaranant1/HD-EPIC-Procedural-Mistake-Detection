from typing import Literal
from pydantic import BaseModel

class MistakeResponse(BaseModel):
    target_index: int
    original_action_text: str
    mistake_action_text: str
    mistake_type: Literal[
        "wrong_ingredient",
        "wrong_tool",
        "wrong_quantity",
        "wrong_order",
        "wrong_temperature",
        "wrong_temperature_time",
        "contamination",
        "other",
    ]
    why_this_action_is_critical: str
    why_goal_breaking: str
    why_observable_now: str
    why_hard_to_recover: str
    why_plausible: str
    detectability: Literal["subtle", "moderate"]
    confidence: Literal["high", "medium", "low"]