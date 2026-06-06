from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_STREAMS = Path("data/processed/hd_epic_procedural_streams.jsonl")
DEFAULT_RESPONSES = Path("data/processed/mistake_injection_llm_outputs.jsonl")
DEFAULT_OUT = Path("data/processed/hd_epic_mistake_streams.jsonl")

REQUIRED_RATIONALE_FIELDS = [
    "why_this_action_is_critical",
    "why_goal_breaking",
    "why_observable_now",
    "why_hard_to_recover",
    "why_plausible",
    "detectability",
    "confidence",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse LLM mistake outputs into chopped streams with binary masks."
    )
    parser.add_argument("--streams", type=Path, default=DEFAULT_STREAMS)
    parser.add_argument("--responses", type=Path, default=DEFAULT_RESPONSES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--response-field",
        default="llm_response",
        help="field containing the raw JSON response from the LLM",
    )
    parser.add_argument(
        "--errors-out",
        type=Path,
        default=None,
        help="optional JSONL path for invalid rows",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit with a nonzero status if any row fails validation",
    )
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_llm_response(row: dict[str, Any], response_field: str) -> dict[str, Any]:
    raw_response = row.get(response_field, row.get("response", row.get("output")))
    if raw_response is None:
        return row
    if isinstance(raw_response, dict):
        return raw_response
    if not isinstance(raw_response, str):
        raise ValueError(f"Expected LLM response text or object, found {type(raw_response)!r}")

    text = raw_response.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("LLM response does not contain a JSON object")
    return json.loads(text[start : end + 1])


def require_nonempty_str(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or empty string field: {field}")
    return value.strip()


def normalize_action_text(text: str) -> str:
    return " ".join(text.split())


def validate_payload(
    payload: dict[str, Any],
    stream: dict[str, Any],
    candidate_indices: list[Any] | None,
) -> dict[str, Any]:
    actions = stream.get("actions", [])
    target_index = payload.get("target_index")
    if not isinstance(target_index, int):
        raise ValueError("target_index must be an integer")
    if target_index < 0 or target_index >= len(actions):
        raise ValueError(f"target_index {target_index} outside action stream length {len(actions)}")

    if candidate_indices:
        valid_indices = {index for index in candidate_indices if isinstance(index, int)}
        if target_index not in valid_indices:
            raise ValueError("target_index is not in candidate_action_indices")

    original_action_text = payload.get("original_action_text")
    expected_text = actions[target_index].get("text", "")
    if not isinstance(original_action_text, str):
        raise ValueError("original_action_text must be a string")
    if normalize_action_text(original_action_text) != normalize_action_text(expected_text):
        raise ValueError("original_action_text does not match the selected source action")

    validated = {
        "target_index": target_index,
        "original_action_text": expected_text,
        "llm_original_action_text": original_action_text,
        "original_action_text_exact_match": original_action_text == expected_text,
        "mistake_action_text": require_nonempty_str(payload, "mistake_action_text"),
        "mistake_type": require_nonempty_str(payload, "mistake_type"),
    }
    for field in REQUIRED_RATIONALE_FIELDS:
        validated[field] = require_nonempty_str(payload, field)
    return validated


def make_mistake_action(stream: dict[str, Any], mistake: dict[str, Any]) -> dict[str, Any]:
    source_action = stream["actions"][mistake["target_index"]]
    action = dict(source_action)
    action["text"] = mistake["mistake_action_text"]
    action["is_mistake"] = True
    action["mistake_type"] = mistake["mistake_type"]
    action["original_action_id"] = source_action.get("action_id")
    action["original_text"] = source_action.get("text")
    return action


def build_mistake_stream(stream: dict[str, Any], mistake: dict[str, Any]) -> dict[str, Any]:
    target_index = mistake["target_index"]
    chopped_actions = [dict(action) for action in stream["actions"][:target_index]]
    chopped_actions.append(make_mistake_action(stream, mistake))

    output = {key: value for key, value in stream.items() if key != "actions"}
    output["stream_id"] = f"{stream['stream_id']}_mistake_{target_index:04d}"
    output["source_stream_id"] = stream["stream_id"]
    output["actions"] = chopped_actions
    output["mistake_mask"] = [0] * target_index + [1]
    output["mistake"] = mistake
    output["original_action_count"] = len(stream["actions"])
    output["truncated_action_count"] = len(chopped_actions)
    output["removed_original_actions_after_mistake"] = len(stream["actions"]) - target_index - 1
    return output


def build_dataset(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    streams_by_id = {stream["stream_id"]: stream for stream in read_jsonl(args.streams)}
    responses = read_jsonl(args.responses)
    outputs = []
    errors = []

    for line_number, row in enumerate(responses, start=1):
        stream_id = row.get("stream_id")
        try:
            if stream_id not in streams_by_id:
                raise ValueError(f"Unknown stream_id: {stream_id!r}")
            payload = parse_llm_response(row, args.response_field)
            mistake = validate_payload(
                payload,
                streams_by_id[stream_id],
                row.get("candidate_action_indices"),
            )
            outputs.append(build_mistake_stream(streams_by_id[stream_id], mistake))
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(
                {
                    "line_number": line_number,
                    "stream_id": stream_id,
                    "error": str(exc),
                    "row": row,
                }
            )

    return outputs, errors


def main() -> None:
    args = parse_args()
    outputs, errors = build_dataset(args)
    write_jsonl(args.out, outputs)
    print(f"Wrote {len(outputs)} final mistake streams to {args.out}")

    if errors:
        errors_out = args.errors_out or args.out.with_suffix(".errors.jsonl")
        write_jsonl(errors_out, errors)
        print(f"Wrote {len(errors)} invalid rows to {errors_out}")
        if args.strict:
            raise SystemExit(1)
    else:
        print(f"No invalid rows.")


if __name__ == "__main__":
    main()
