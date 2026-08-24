from pathlib import Path

import pytest

from soundcloudopen.downloader import build_command, validate_soundcloud_url


def test_accepts_soundcloud_playlist():
    url = "https://soundcloud.com/example/sets/all-songs"
    assert validate_soundcloud_url(url) == url


def test_rejects_non_soundcloud_url():
    with pytest.raises(ValueError):
        validate_soundcloud_url("https://example.com/file.mp3")


def test_exact_download_features_are_enabled(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("soundcloudopen.downloader.detect_browser", lambda: "chrome")
    cmd = build_command(
        "https://soundcloud.com/example/sets/all-songs",
        tmp_path,
        browser="auto",
    )
    joined = " ".join(cmd)
    assert "--yes-playlist" in cmd
    assert "--ignore-errors" in cmd
    assert "--continue" in cmd
    assert "--no-overwrites" in cmd
    assert "--write-thumbnail" in cmd
    assert "--convert-thumbnails" in cmd
    assert "--embed-thumbnail" in cmd
    assert "--embed-metadata" in cmd
    assert "--extract-audio" in cmd
    assert "--audio-format" in cmd
    assert "mp3" in cmd
    assert "--cookies-from-browser" in cmd
    assert "chrome" in cmd
    assert "thumbnail:" in joined
    assert "Artwork" in joined
