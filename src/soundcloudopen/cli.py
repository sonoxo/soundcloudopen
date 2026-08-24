from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

from . import __version__
from .downloader import (
    SUPPORTED_BROWSERS,
    build_command,
    check_dependencies,
    default_output_dir,
    detect_browser,
    run_command,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="soundcloudopen",
        description="Bulk-download a SoundCloud playlist with track artwork using yt-dlp.",
    )
    p.add_argument("url", nargs="?", help="SoundCloud track or playlist URL")
    p.add_argument("-o", "--output", type=Path, default=default_output_dir(), help="Output directory")
    p.add_argument("--browser", choices=SUPPORTED_BROWSERS, default="auto", help="Browser cookies for private playlists (default: auto)")
    p.add_argument("--format", choices=("mp3", "m4a", "opus", "flac", "wav", "aac"), default="mp3", dest="audio_format")
    p.add_argument("--save-json", action="store_true", help="Also save yt-dlp metadata JSON")
    p.add_argument("--list", action="store_true", dest="flat_playlist", help="List playlist entries without downloading")
    p.add_argument("--print-command", action="store_true", help="Print the yt-dlp command without running it")
    p.add_argument("--check", action="store_true", help="Check yt-dlp, ffmpeg and browser detection")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)

    if args.check:
        missing = check_dependencies()
        browser = detect_browser()
        print(f"yt-dlp: {'OK' if 'yt-dlp' not in missing else 'MISSING'}")
        print(f"ffmpeg: {'OK' if 'ffmpeg' not in missing else 'MISSING'}")
        print(f"browser: {browser or 'not detected'}")
        return 1 if missing else 0

    if not args.url:
        parser().error("a SoundCloud URL is required unless --check is used")

    missing = check_dependencies()
    if missing and not args.print_command:
        print("Missing required dependency/dependencies: " + ", ".join(missing), file=sys.stderr)
        print("Run the installer for your OS or see README.md.", file=sys.stderr)
        return 2

    try:
        command = build_command(
            url=args.url,
            output_dir=args.output,
            browser=args.browser,
            audio_format=args.audio_format,
            save_json=args.save_json,
            flat_playlist=args.flat_playlist,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.print_command:
        print(shlex.join(command))
        return 0

    args.output.expanduser().mkdir(parents=True, exist_ok=True)
    selected = args.browser if args.browser != "auto" else (detect_browser() or "none")
    print(f"SoundCloudOpen v{__version__}")
    print(f"Output: {args.output.expanduser()}")
    print(f"Browser cookies: {selected}")
    return run_command(command)
