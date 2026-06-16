import json
import os
from pathlib import Path
import time

from google import genai
from schemas import MistakeResponse

# Config
Model = "gemini-flash-lite-latest"
Temperature = 0.25

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

requests_path = Path("prompts/mistake_injection_prompts.jsonl")
out_path = Path(f"data/processed/mistake_injection_llm_outputs.jsonl")

with requests_path.open(encoding="utf-8") as inp, out_path.open("w", encoding="utf-8") as out:
    # avoid rate limits by spacing out requests
    i = 0
    for index, line in enumerate(inp, start=1):
        i+=1
        if i % 6 == 0:
            print(f"Sleeping for 60 seconds to avoid rate limits...")
            time.sleep(60)

        row = json.loads(line)
        print(f"{index}: generating mistake for {row['stream_id']}")

        response = client.models.generate_content(
            model=Model,
            contents=row["prompt"],
            config={
                "temperature": Temperature,
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
