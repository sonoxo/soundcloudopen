from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import __version__
from .downloader import validate_soundcloud_url

BEATSTARS_MCP_URL = "https://mcp.beatstars.com/mcp"
MODE = "XUNIA_SOUNDS_3LM_CLAUDE_BEATSTARS_VIRGINIA"
MAX_RESULTS = 10


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def build_discovery_prompt(
    prompt: str,
    *,
    bpm: int | None = None,
    genre: str | None = None,
    mood: str | None = None,
    use_case: str | None = None,
    count: int = 5,
) -> str:
    """Expand a simple creative request into a BeatStars-friendly natural-language search."""
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("A BeatStars discovery prompt is required")
    if bpm is not None and not 1 <= bpm <= 400:
        raise ValueError("BPM must be between 1 and 400")
    if not 1 <= count <= MAX_RESULTS:
        raise ValueError(f"Result count must be between 1 and {MAX_RESULTS}")

    details: list[str] = [prompt]
    if genre := _clean_optional(genre):
        details.append(f"genre: {genre}")
    if mood := _clean_optional(mood):
        details.append(f"mood: {mood}")
    if bpm is not None:
        details.append(f"around {bpm} BPM")
    if use_case := _clean_optional(use_case):
        details.append(f"intended use: {use_case}")

    joined = "; ".join(details)
    return (
        f"Find {count} beats on BeatStars that match this creative direction: {joined}. "
        "Use BeatStars intelligent natural-language discovery, let me preview the matching beats in Claude, "
        "briefly explain why each candidate fits, and include a BeatStars page handoff so I can review the full beat "
        "and the producer's current license terms before using it."
    )


def build_xunia_mission(
    prompt: str,
    *,
    soundcloud_url: str | None = None,
    audio_format: str = "mp3",
    bpm: int | None = None,
    genre: str | None = None,
    mood: str | None = None,
    use_case: str | None = None,
    count: int = 5,
) -> dict[str, Any]:
    """Build a portable XUNIA SOUNDS mission without making network calls.

    BeatStars connectivity is delegated to Claude's remote MCP connector so OAuth
    and permissions stay in the service that owns them. SoundCloudOpen only
    handles SoundCloud URLs the user is allowed to save.
    """
    search_prompt = build_discovery_prompt(
        prompt,
        bpm=bpm,
        genre=genre,
        mood=mood,
        use_case=use_case,
        count=count,
    )

    soundcloud: dict[str, Any] | None = None
    if soundcloud_url:
        soundcloud = {
            "url": validate_soundcloud_url(soundcloud_url),
            "role": "authorized-media-source",
            "audioFormat": audio_format,
        }

    filters = {
        "genre": _clean_optional(genre),
        "mood": _clean_optional(mood),
        "bpm": bpm,
        "useCase": _clean_optional(use_case),
        "requestedResults": count,
    }

    return {
        "mode": MODE,
        "beginnerSummary": (
            "Describe the sound you want, let Claude search BeatStars through its MCP connector, preview the matches, "
            "open the beat you like on BeatStars to review the producer's license, then use SoundCloudOpen only for "
            "SoundCloud media you own or are allowed to save."
        ),
        "virginia": {
            "intent": prompt.strip(),
            "searchPrompt": search_prompt,
            "steps": [
                "DESCRIBE_SOUND",
                "EXPAND_DISCOVERY_INTENT",
                "SEARCH_BEATSTARS_INTELLIGENTLY",
                "PREVIEW_CANDIDATES_IN_CLAUDE",
                "EXPLAIN_MATCHES",
                "OPEN_SELECTED_BEAT_PAGE",
                "REVIEW_PRODUCER_LICENSE",
                "IMPORT_AUTHORIZED_SOUNDCLOUD_MEDIA" if soundcloud else "KEEP_SOUNDCLOUD_OPTIONAL",
                "RETURN_XUNIA_SOUNDS_EVIDENCE",
            ],
        },
        "claude": {
            "mode": "3LM CLAUDE",
            "role": "conversation-and-tool-orchestrator",
            "expectedExperience": [
                "send natural-language discovery intent to the BeatStars connector",
                "show matching BeatStars results that can be previewed in Claude",
                "explain why each result fits the request",
                "hand off the selected result to its BeatStars page",
            ],
        },
        "beatstars": {
            "transport": "remote-mcp",
            "endpoint": BEATSTARS_MCP_URL,
            "intent": prompt.strip(),
            "naturalLanguagePrompt": search_prompt,
            "filters": filters,
            "capability": "BeatStars intelligent search through server-defined tools discovered by Claude at connection time",
            "licenseHandoff": (
                "Open the selected beat on BeatStars and review the producer's current license terms before use. "
                "License terms and pricing are controlled by the producer and can vary by beat."
            ),
        },
        "soundcloud": soundcloud,
        "evidence": {
            "return": [
                "discovery prompt",
                "requested filters",
                "candidate rationale",
                "selected BeatStars page handoff",
                "license-review-required state",
                "optional authorized SoundCloud source",
            ]
        },
        "guardrails": {
            "beatstars": "Do not treat the MCP connector as an undocumented upload API or assume a license without reviewing the producer's current terms.",
            "soundcloud": "Only save audio you own, downloads SoundCloud permits, or material you otherwise have permission to save.",
        },
    }


def claude_connector_steps() -> list[str]:
    return [
        "Open Claude → Customize → Connectors.",
        "Choose + → Add custom connector.",
        "Name it BeatStars.",
        f"Use the remote MCP URL: {BEATSTARS_MCP_URL}",
        "Click Add, then Connect, and approve the BeatStars permissions shown by Claude.",
        "Enable BeatStars for the conversation where you use XUNIA SOUNDS.",
    ]


def render_connector_guide() -> str:
    lines = ["XUNIA SOUNDS // 3LM CLAUDE // BEATSTARS // VIRGINIA", ""]
    lines.extend(f"{index}. {step}" for index, step in enumerate(claude_connector_steps(), start=1))
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="xunia-sounds",
        description="Build a beginner-friendly XUNIA SOUNDS mission connecting SoundCloudOpen with BeatStars through Claude MCP.",
    )
    p.add_argument("prompt", nargs="?", help="Natural-language description of the beat or sound you want to discover")
    p.add_argument("--soundcloud", dest="soundcloud_url", help="Optional authorized SoundCloud track or playlist URL")
    p.add_argument("--format", choices=("mp3", "m4a", "opus", "flac", "wav", "aac"), default="mp3", dest="audio_format")
    p.add_argument("--bpm", type=int, help="Optional target BPM")
    p.add_argument("--genre", help="Optional genre hint")
    p.add_argument("--mood", help="Optional mood or energy hint")
    p.add_argument("--use-case", dest="use_case", help="Optional intended use, such as demo, album, video, or paid ad")
    p.add_argument("--count", type=int, default=5, help=f"Number of BeatStars candidates to request (1-{MAX_RESULTS})")
    p.add_argument("--prompt-only", action="store_true", help="Print only the expanded BeatStars discovery prompt for Claude")
    p.add_argument("--json", type=Path, dest="json_path", help="Also write the mission JSON to this file")
    p.add_argument("--claude-setup", action="store_true", help="Print the BeatStars remote MCP connector setup steps for Claude")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)

    if args.claude_setup:
        print(render_connector_guide())
        return 0

    if not args.prompt:
        parser().error("a discovery prompt is required unless --claude-setup is used")

    try:
        mission = build_xunia_mission(
            args.prompt,
            soundcloud_url=args.soundcloud_url,
            audio_format=args.audio_format,
            bpm=args.bpm,
            genre=args.genre,
            mood=args.mood,
            use_case=args.use_case,
            count=args.count,
        )
    except ValueError as exc:
        parser().error(str(exc))

    if args.prompt_only:
        print(mission["beatstars"]["naturalLanguagePrompt"])
        return 0

    payload = json.dumps(mission, indent=2, ensure_ascii=False)
    print(payload)

    if args.json_path:
        path = args.json_path.expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
