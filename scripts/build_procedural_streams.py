"""Convert HD-EPIC annotations into simple procedural action streams."""

from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path
from typing import Any

import pandas as pd


class NumpyCompatUnpickler(pickle.Unpickler):
    """Read HD-EPIC pickle files saved with NumPy 2 module paths."""

    def find_class(self, module: str, name: str) -> Any:
        if module == "numpy._core.multiarray":
            module = "numpy.core.multiarray"
        elif module == "numpy._core.numeric":
            module = "numpy.core.numeric"
        return super().find_class(module, name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--annotations-dir",
        type=Path,
        default=Path("data/raw/hd-epic-annotations"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/processed/hd_epic_procedural_streams.jsonl"),
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_narrations(path: Path) -> pd.DataFrame:
    with path.open("rb") as handle:
        df = NumpyCompatUnpickler(handle).load()
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected DataFrame in {path}, found {type(df)!r}")
    return df.sort_values(["video_id", "start_timestamp", "end_timestamp"])


def safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_json(value: Any) -> Any:
    if isinstance(value, tuple):
        return [clean_json(item) for item in value]
    if isinstance(value, list):
        return [clean_json(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def add_segments(
    segments: list[dict[str, Any]],
    raw_segments: list[dict[str, Any]],
    *,
    kind: str,
    label: str,
    step_id: str | None = None,
    ingredient_id: str | None = None,
) -> None:
    for raw in raw_segments:
        start = safe_float(raw.get("start"))
        end = safe_float(raw.get("end"))
        video_id = raw.get("video")
        if video_id is None or start is None or end is None:
            continue
        segments.append(
            {
                "video_id": video_id,
                "start": start,
                "end": end,
                "kind": kind,
                "label": label,
                "step_id": step_id,
                "ingredient_id": ingredient_id,
            }
        )


def collect_procedure_segments(recipe: dict[str, Any], capture: dict[str, Any]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    steps = recipe.get("steps", {})

    for step_id, raw_segments in capture.get("step_times", {}).items():
        add_segments(
            segments,
            raw_segments,
            kind="recipe_step",
            label=steps.get(step_id, ""),
            step_id=step_id,
        )

    for step_id, raw_segments in capture.get("prep_times", {}).items():
        add_segments(
            segments,
            raw_segments,
            kind="recipe_prep",
            label=steps.get(step_id, ""),
            step_id=step_id,
        )

    for ingredient_id, ingredient in capture.get("ingredients", {}).items():
        ingredient_name = ingredient.get("name", "")
        add_segments(
            segments,
            ingredient.get("add", []),
            kind="ingredient_add",
            label=ingredient_name,
            ingredient_id=ingredient_id,
        )
        add_segments(
            segments,
            ingredient.get("weigh", []),
            kind="ingredient_weigh",
            label=ingredient_name,
            ingredient_id=ingredient_id,
        )

    return segments


def windows_from_segments(
    videos: list[str],
    segments: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    windows: dict[str, dict[str, float]] = {}
    for video_id in videos:
        video_segments = [segment for segment in segments if segment["video_id"] == video_id]
        if not video_segments:
            continue
        windows[video_id] = {
            "start": min(segment["start"] for segment in video_segments),
            "end": max(segment["end"] for segment in video_segments),
        }
    return windows


def actions_for_windows(
    narrations: pd.DataFrame,
    videos: list[str],
    windows: dict[str, dict[str, float]],
) -> list[dict[str, Any]]:
    rows = []
    video_order = {video_id: index for index, video_id in enumerate(videos)}

    for video_id in videos:
        window = windows.get(video_id)
        if window is None:
            continue
        video_rows = narrations[
            (narrations["video_id"] == video_id)
            & (narrations["end_timestamp"] >= window["start"])
            & (narrations["start_timestamp"] <= window["end"])
        ]
        rows.extend(video_rows.to_dict(orient="records"))

    rows.sort(
        key=lambda row: (
            video_order.get(row["video_id"], 10_000),
            row["start_timestamp"],
            row["end_timestamp"],
        )
    )

    actions = []
    for idx, row in enumerate(rows):
        actions.append(
            {
                "idx": idx,
                "action_id": str(row["unique_narration_id"]),
                "video_id": str(row["video_id"]),
                "start": float(row["start_timestamp"]),
                "end": float(row["end_timestamp"]),
                "text": str(row["narration"]),
                "verbs": clean_json(row.get("verbs", [])),
                "nouns": clean_json(row.get("nouns", [])),
                "main_actions": clean_json(row.get("main_actions", [])),
            }
        )
    return actions


def build_streams(annotations_dir: Path) -> list[dict[str, Any]]:
    recipes = read_json(annotations_dir / "high-level" / "complete_recipes.json")
    narrations = read_narrations(
        annotations_dir / "narrations-and-action-segments" / "HD_EPIC_Narrations.pkl"
    )

    streams: list[dict[str, Any]] = []
    for recipe_id, recipe in sorted(recipes.items()):
        participant_id = recipe.get("participant", recipe_id.split("_")[0])
        recipe_name = recipe.get("name", recipe_id)
        for capture_index, capture in enumerate(recipe.get("captures", []), start=1):
            videos = capture.get("videos", [])
            segments = collect_procedure_segments(recipe, capture)
            windows = windows_from_segments(videos, segments)
            if not windows:
                continue

            actions = actions_for_windows(narrations, videos, windows)
            if not actions:
                continue

            streams.append(
                {
                    "stream_id": f"{recipe_id}_C{capture_index:02d}",
                    "dataset": "HD-EPIC",
                    "participant_id": participant_id,
                    "recipe_id": recipe_id,
                    "capture_index": capture_index,
                    "goal": f"prepare {recipe_name}",
                    "goal_source": "hd_epic_complete_recipes",
                    "videos": videos,
                    "window_by_video": windows,
                    "recipe_steps": [
                        {"step_id": step_id, "text": text}
                        for step_id, text in recipe.get("steps", {}).items()
                    ],
                    "procedure_segments": segments,
                    "actions": actions,
                }
            )

    return streams


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    streams = build_streams(args.annotations_dir)
    write_jsonl(args.out, streams)
    print(f"Wrote {len(streams)} procedural streams to {args.out}")


if __name__ == "__main__":
    main()

