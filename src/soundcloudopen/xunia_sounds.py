from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import __version__
from .downloader import validate_soundcloud_url

BEATSTARS_MCP_URL = "https://mcp.beatstars.com/mcp"
MODE = "XUNIA_SOUNDS_3LM_CLAUDE_BEATSTARS_VIRGINIA"


def build_xunia_mission(
    prompt: str,
    *,
    soundcloud_url: str | None = None,
    audio_format: str = "mp3",
) -> dict[str, Any]:
    """Build a portable XUNIA SOUNDS mission without making network calls.

    BeatStars connectivity is delegated to Claude's remote MCP connector so OAuth
    and permissions stay in the service that owns them. SoundCloudOpen only
    handles SoundCloud URLs the user is allowed to save.
    """
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("A BeatStars discovery prompt is required")

    soundcloud: dict[str, Any] | None = None
    if soundcloud_url:
        soundcloud = {
            "url": validate_soundcloud_url(soundcloud_url),
            "role": "authorized-media-source",
            "audioFormat": audio_format,
        }

    return {
        "mode": MODE,
        "beginnerSummary": (
            "Describe the sound you want, let Claude search BeatStars through its MCP connector, "
            "choose and license a beat on BeatStars when needed, then use SoundCloudOpen only for "
            "SoundCloud media you own or are allowed to save."
        ),
        "virginia": {
            "intent": prompt,
            "steps": [
                "DESCRIBE_SOUND",
                "SEARCH_BEATSTARS",
                "REVIEW_CANDIDATES",
                "LICENSE_IF_NEEDED",
                "IMPORT_AUTHORIZED_SOUNDCLOUD_MEDIA" if soundcloud else "KEEP_SOUNDCLOUD_OPTIONAL",
                "RETURN_XUNIA_SOUNDS_EVIDENCE",
            ],
        },
        "claude": {
            "mode": "3LM CLAUDE",
            "role": "conversation-and-tool-orchestrator",
        },
        "beatstars": {
            "transport": "remote-mcp",
            "endpoint": BEATSTARS_MCP_URL,
            "intent": prompt,
            "capability": "server-defined BeatStars tools discovered by Claude at connection time",
            "licenseHandoff": "Open the selected beat on BeatStars to review and obtain the required license.",
        },
        "soundcloud": soundcloud,
        "guardrails": {
            "beatstars": "Do not treat the MCP connector as an undocumented upload API.",
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
        )
    except ValueError as exc:
        parser().error(str(exc))

    payload = json.dumps(mission, indent=2, ensure_ascii=False)
    print(payload)

    if args.json_path:
        path = args.json_path.expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
