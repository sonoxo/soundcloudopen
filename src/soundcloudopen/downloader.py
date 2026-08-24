from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

SUPPORTED_BROWSERS = (
    "auto",
    "none",
    "chrome",
    "chromium",
    "firefox",
    "edge",
    "brave",
    "opera",
    "vivaldi",
    "safari",
)


def validate_soundcloud_url(url: str) -> str:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")
    if host not in {"soundcloud.com", "www.soundcloud.com", "m.soundcloud.com"}:
        raise ValueError("URL must be a soundcloud.com URL")
    return url.strip()


def default_output_dir() -> Path:
    return Path.home() / "Music" / "SoundCloud"


def _candidate_browser_paths() -> dict[str, list[Path]]:
    home = Path.home()
    system = platform.system().lower()
    if system == "darwin":
        return {
            "chrome": [Path("/Applications/Google Chrome.app")],
            "brave": [Path("/Applications/Brave Browser.app")],
            "edge": [Path("/Applications/Microsoft Edge.app")],
            "firefox": [Path("/Applications/Firefox.app")],
            "safari": [Path("/Applications/Safari.app")],
            "chromium": [Path("/Applications/Chromium.app")],
            "opera": [Path("/Applications/Opera.app")],
            "vivaldi": [Path("/Applications/Vivaldi.app")],
        }
    if system == "windows":
        local = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        program_files = Path(os.environ.get("PROGRAMFILES", "C:/Program Files"))
        program_files_x86 = Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)"))
        return {
            "chrome": [local / "Google/Chrome/User Data", program_files / "Google/Chrome/Application"],
            "edge": [local / "Microsoft/Edge/User Data", program_files_x86 / "Microsoft/Edge/Application"],
            "brave": [local / "BraveSoftware/Brave-Browser/User Data"],
            "firefox": [home / "AppData/Roaming/Mozilla/Firefox/Profiles"],
            "chromium": [local / "Chromium/User Data"],
            "opera": [home / "AppData/Roaming/Opera Software"],
            "vivaldi": [local / "Vivaldi/User Data"],
        }
    return {
        "chrome": [home / ".config/google-chrome"],
        "chromium": [home / ".config/chromium"],
        "firefox": [home / ".mozilla/firefox"],
        "edge": [home / ".config/microsoft-edge"],
        "brave": [home / ".config/BraveSoftware/Brave-Browser"],
        "opera": [home / ".config/opera"],
        "vivaldi": [home / ".config/vivaldi"],
    }


def detect_browser() -> str | None:
    for browser, paths in _candidate_browser_paths().items():
        if any(path.exists() for path in paths):
            return browser
    return None


def check_dependencies() -> list[str]:
    missing: list[str] = []
    if shutil.which("yt-dlp") is None:
        missing.append("yt-dlp")
    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg")
    return missing


def build_command(
    url: str,
    output_dir: Path,
    browser: str = "auto",
    audio_format: str = "mp3",
    save_json: bool = False,
    flat_playlist: bool = False,
) -> list[str]:
    url = validate_soundcloud_url(url)
    output_dir = output_dir.expanduser().resolve()

    cmd = ["yt-dlp"]

    selected_browser = browser
    if browser == "auto":
        selected_browser = detect_browser() or "none"
    if selected_browser != "none":
        cmd += ["--cookies-from-browser", selected_browser]

    if flat_playlist:
        cmd += ["--flat-playlist", "--print", "%(playlist_index)s\t%(title)s\t%(url)s"]
    else:
        cmd += [
            "--yes-playlist",
            "--ignore-errors",
            "--continue",
            "--no-overwrites",
            "--write-thumbnail",
            "--convert-thumbnails",
            "jpg",
            "--embed-thumbnail",
            "--embed-metadata",
            "--extract-audio",
            "--audio-format",
            audio_format,
            "--audio-quality",
            "0",
        ]
        if save_json:
            cmd.append("--write-info-json")

        track_template = str(
            output_dir
            / "%(playlist_title|SoundCloud)s"
            / "%(playlist_index)03d - %(uploader)s - %(title)s.%(ext)s"
        )
        art_template = str(
            output_dir
            / "%(playlist_title|SoundCloud)s"
            / "Artwork"
            / "%(playlist_index)03d - %(uploader)s - %(title)s.%(ext)s"
        )
        cmd += ["-o", track_template, "-o", f"thumbnail:{art_template}"]

    cmd.append(url)
    return cmd


def run_command(command: Iterable[str]) -> int:
    process = subprocess.run(list(command), shell=False, check=False)
    return int(process.returncode)
