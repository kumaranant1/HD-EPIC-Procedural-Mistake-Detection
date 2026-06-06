"""

Prepare prompts for procedural mistake injection using LLMs.

The LLM will choose one critical action near the middle of an procedural stream
and rewrites that action into a plausible, goal-breaking mistake.

"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_STREAMS = Path("data/processed/hd_epic_procedural_streams.jsonl")
DEFAULT_PROMPTS_OUT = Path("prompts/mistake_injection_prompts.jsonl")

MISTAKE_TYPES = [
    "wrong_ingredient",
    "wrong_tool",
    "wrong_quantity",
    "wrong_order",
    "wrong_temperature",
    "wrong_temperature_time",
    "contamination",
    "other",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create provider-neutral LLM prompts for controlled mistake injection."
        )
    )
    subparsers = parser.add_subparsers(dest="command")

    prompts = subparsers.add_parser("prompts", help="write LLM prompt jobs")
    prompts.add_argument("--streams", type=Path, default=DEFAULT_STREAMS)
    prompts.add_argument("--out", type=Path, default=DEFAULT_PROMPTS_OUT)
    prompts.add_argument("--limit", type=int, default=None)
    prompts.add_argument("--min-actions", type=int, default=8)
    prompts.add_argument("--position-ratio", type=float, default=0.5)
    prompts.add_argument(
        "--candidate-window-ratio",
        type=float,
        default=0.3,
        help="fraction of the sequence on each side of the midpoint to show as candidates",
    )
    prompts.add_argument(
        "--max-candidate-actions",
        type=int,
        default=160,
        help="maximum number of candidate actions to show; use 0 for no cap",
    )
    prompts.add_argument("--context-before", type=int, default=8)
    prompts.add_argument("--context-after", type=int, default=8)

    argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        argv = ["prompts", *argv]
    return parser.parse_args(argv)


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


def action_line(action: dict[str, Any]) -> str:
    return f"{action['idx']}. {action['text']}"


def action_lines(actions: list[dict[str, Any]]) -> str:
    if not actions:
        return "(none)"
    return "\n".join(action_line(action) for action in actions)


def recipe_step_lines(stream: dict[str, Any]) -> str:
    steps = stream.get("recipe_steps", [])
    if not steps:
        return "(none)"
    return "\n".join(f"- {step['text']}" for step in steps)


def midpoint_index(action_count: int, position_ratio: float) -> int:
    if action_count <= 0:
        raise ValueError("Cannot choose a midpoint for an empty action stream")
    ratio = min(max(position_ratio, 0.0), 1.0)
    midpoint = round((action_count - 1) * ratio)
    if action_count >= 3:
        return min(max(midpoint, 1), action_count - 2)
    return midpoint


def candidate_bounds(
    action_count: int,
    *,
    position_ratio: float,
    candidate_window_ratio: float,
    max_candidate_actions: int,
) -> tuple[int, int, int]:
    midpoint = midpoint_index(action_count, position_ratio)
    if action_count < 3:
        return midpoint, midpoint, midpoint

    window_ratio = min(max(candidate_window_ratio, 0.0), 1.0)
    radius = max(1, round(action_count * window_ratio))
    if max_candidate_actions > 0:
        radius = min(radius, max(1, (max_candidate_actions - 1) // 2))
    start = max(1, midpoint - radius)
    end = min(action_count - 2, midpoint + radius)
    return start, end, midpoint


def build_mistake_prompt(
    stream: dict[str, Any],
    *,
    candidate_start: int,
    candidate_end: int,
    midpoint: int,
    context_before: int,
    context_after: int,
) -> str:
    actions = stream.get("actions", [])
    candidates = actions[candidate_start : candidate_end + 1]
    before_start = max(0, candidate_start - context_before)
    after_end = min(len(actions), candidate_end + context_after + 1)
    previous_context = actions[before_start:candidate_start]
    future_context = actions[candidate_end + 1 : after_end]
    candidate_indices = [action["idx"] for action in candidates]
    mistake_types = ", ".join(MISTAKE_TYPES)

    return f"""You are creating one controlled counterfactual mistake for online procedural mistake detection.

Goal:
{stream.get("goal", "")}

High-level recipe steps, for reference only:
{recipe_step_lines(stream)}

The action stream has {len(actions)} actions. The approximate midpoint is action index {midpoint}.
Choose exactly one critical action from the candidate actions near this midpoint.

For this task, a critical action means a committed recipe-state change: an action where an ingredient, food item, tool, heat source, cooking vessel, or appliance is used in a way that directly changes the recipe outcome right now. Changing this action should be hard to recover from, not something the person can simply undo in the next moment or reinterpret as a different harmless side task.

Good critical targets usually look like:
- adding, pouring, sprinkling, mixing, stirring, draining, discarding, transferring, or combining ingredients into the actual recipe mixture or cooking vessel
- putting food or liquid into a specific cooking vessel, appliance, oven, pan, pot, fridge, or freezer when that placement directly changes the recipe state
- applying heat, choosing cooking temperature or time, starting a cooking/blending/frothing process after ingredients are committed
- using a tool that directly transforms the food, such as cutting, blending, grinding, straining, or frothing

Noise/support actions are not valid targets. Leave these unchanged:
- opening or closing doors, cupboards, drawers, packets, lids, fridges, or appliance doors
- picking up, putting down, holding, moving, checking, looking at, or arranging objects before they are used
- plugging, unplugging, switching power on/off, pressing generic power buttons, or moving cables
- cleaning, wiping, tidying, drinking water, using a phone, walking, waiting, or repositioning the body/camera
- selecting or picking up an ingredient without adding it to the recipe yet
- staging or holding ingredients in a temporary mug, glass, bowl, plate, or container before they enter the recipe
- pouring something into a separate container if it could plausibly be for another harmless use

Example: replacing "pick up a jar of spices" with "pick up sugar" is not a good mistake, because the person could notice before adding it. Replacing "add the spices into the pan" with "add sugar into the pan" is a good mistake, because the wrong ingredient has been committed to the recipe.
Example: replacing "pour hot water into a mug" with "pour vinegar into a mug" is not a good mistake unless that mug is already the recipe mixture or final food state. The person could be preparing something else, and the bad ingredient has not entered the recipe yet.
Example: replacing "pour milk into the frother" with "pour milk into the mug" is usually not a good mistake, because the milk may still be transferable or the mug may be part of the coffee workflow. Prefer a replacement like adding the wrong ingredient into the frother, adding the milk into an already incompatible mixture, overheating it, contaminating it, or using a directly recipe-breaking quantity.

Previous context before the candidate window (this is the previous partial context). These actions will remain unchanged:
{action_lines(previous_context)}

Candidate actions. Choose exactly one target_index from this list:
{action_lines(candidates)}

Future reference actions from the original stream (this is the future partial context). These will be removed after the changed action; use them only to understand what the procedure was trying to accomplish:
{action_lines(future_context)}

Task:
1. Select the most suitable critical action from candidate_action_indices: {candidate_indices}.
2. Replace only that action with one plausible action-level mistake.
3. Do not insert actions. Do not delete actions before the selected target.
4. If many candidate actions are noise/support actions, ignore them and choose the best committed recipe-state action that remains in the candidate list.

Rules:
- The replacement must be a natural HD-EPIC-style action narration, not an explanation.
- The replacement must be plausible given the previous context.
- The replacement must break or seriously threaten the goal.
- Do not choose actions from parallel side tasks, even if they involve food, ingredients, bowls, mugs, or utensils. A candidate action is valid only if it directly advances the stated goal or one of the recipe steps.
- If an action prepares or modifies another food/drink not mentioned in the goal or recipe steps, treat it as natural noise. Leave it unchanged.
- The mistake must be observable as goal-breaking at this action, not only after assuming a later future action.
- Prefer mistakes that commit the wrong ingredient/tool/quantity/order/temperature/contamination into the recipe state.
- The mistake should be hard to recover from without restarting, discarding food, removing mixed ingredients, or substantially redoing the procedure.
- Do not choose reversible setup/support actions such as picking something up, opening/closing, plugging/unplugging, switching power, or pressing generic power buttons.
- Do not create mistakes that only move the correct ingredient into a different clean temporary container.
- Do not create mistakes whose only problem is "this might be used wrongly later."
- The replacement must not be a harmless variation, preference, or common valid alternative.
- The replacement must not be a wild or cartoonish failure. It should look like a realistic human procedural slip: wrong ingredient added, wrong tool used on food, wrong cooking medium, wrong amount, wrong temperature, wrong time, wrong order after a commitment point, or contamination.
- The replacement must not be trivially detectable from wording alone. Avoid words like "mistake", "wrongly", "accidentally", "fails", or "error" in the action text.
- Do not use cartoonish failures such as dropping everything, leaving the kitchen, destroying equipment, unplugging everything, or doing nothing.
- Do not modify the recipe steps. leave them as they are, even if they no longer match the changed action.
- Do not add any second mistake.
- After this one replacement in the candidate actions, the stream will be truncated, so do not describe recovery or later correction.

Rationale fields:
- why_this_action_is_critical: explain why the selected original action directly controls the recipe outcome, not just scene setup.
- why_goal_breaking: explain how the replacement prevents or seriously damages the stated goal.
- why_observable_now: explain why the replacement is already a mistake at this action, without relying on an assumed later action.
- why_hard_to_recover: explain why the changed recipe state cannot be easily undone by the next action.
- why_plausible: explain why a real person could plausibly make this slip in the given context.

(Example response format) Return JSON only, with this exact schema:
{{
  "target_index": {midpoint},
  "original_action_text": "",
  "mistake_action_text": "",
  "mistake_type": "wrong_ingredient",
  "why_this_action_is_critical": "",
  "why_goal_breaking": "",
  "why_observable_now": "",
  "why_hard_to_recover": "",
  "why_plausible": "",
  "detectability": "subtle",
  "confidence": "high"
}}

Schema constraints:
- target_index must be one of: {candidate_indices}.
- original_action_text must exactly match the selected candidate action text.
- mistake_type must be one of: {mistake_types}.
- Use wrong_ingredient only when the ingredient is actually added, poured, mixed, sprinkled, or otherwise committed to the food.
- Use wrong_tool only when the tool directly transforms or contacts the food.
- Use wrong_temperature for incorrect heat level, appliance mode, or temperature setting.
- Use wrong_temperature_time for incorrect cooking/heating/chilling duration.
- detectability must be "subtle" or "moderate"; avoid obvious mistakes.
- confidence must be "high", "medium", or "low".
"""


def make_prompt_jobs(args: argparse.Namespace) -> list[dict[str, Any]]:
    streams = read_jsonl(args.streams)
    if args.limit is not None:
        streams = streams[: args.limit]

    jobs = []
    for stream in streams:
        actions = stream.get("actions", [])
        if len(actions) < args.min_actions:
            continue
        candidate_start, candidate_end, midpoint = candidate_bounds(
            len(actions),
            position_ratio=args.position_ratio,
            candidate_window_ratio=args.candidate_window_ratio,
            max_candidate_actions=args.max_candidate_actions,
        )
        candidate_indices = list(range(candidate_start, candidate_end + 1))
        jobs.append(
            {
                "stream_id": stream["stream_id"],
                "goal": stream.get("goal", ""),
                "sequence_length": len(actions),
                "midpoint_index": midpoint,
                "candidate_start": candidate_start,
                "candidate_end": candidate_end,
                "candidate_action_indices": candidate_indices,
                "max_candidate_actions": args.max_candidate_actions,
                "target_selection_policy": "LLM chooses one critical action from candidate_action_indices",
                "mask_policy": "0 for original prefix actions, 1 for the replaced mistake action",
                "cut_policy": "truncate immediately after the single changed action",
                "prompt": build_mistake_prompt(
                    stream,
                    candidate_start=candidate_start,
                    candidate_end=candidate_end,
                    midpoint=midpoint,
                    context_before=args.context_before,
                    context_after=args.context_after,
                ),
            }
        )
    return jobs


def main() -> None:
    args = parse_args()

    if args.command == "prompts":
        jobs = make_prompt_jobs(args)
        write_jsonl(args.out, jobs)
        print(f"Wrote {len(jobs)} mistake-injection prompt jobs to {args.out}")
        return

    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
