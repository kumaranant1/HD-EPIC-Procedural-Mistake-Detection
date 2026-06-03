import json
import os
from pathlib import Path
from typing import Literal
import time

from google import genai
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


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

requests_path = Path("data/processed/mistake_injection_requests.jsonl")
out_path = Path("data/processed/mistake_injection_llm_outputs.jsonl")

with requests_path.open(encoding="utf-8") as inp, out_path.open("w", encoding="utf-8") as out:
    # avoid rate limits by spacing out requests, and also to give a sense of progress
    i = 0
    for index, line in enumerate(inp, start=1):
        i+=1
        if i % 76 == 0:
            print(f"Sleeping for 60 seconds to avoid rate limits...")
            time.sleep(60)

        row = json.loads(line)
        print(f"{index}: generating mistake for {row['stream_id']}")

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=row["prompt"],
            config={
                "temperature": 0.25,
                "response_mime_type": "application/json",
                "response_schema": MistakeResponse,
            },
        )

        out.write(json.dumps({
            "stream_id": row["stream_id"],
            "candidate_action_indices": row["candidate_action_indices"],
            "llm_response": response.text,
        }, ensure_ascii=False) + "\n")
        out.flush()
