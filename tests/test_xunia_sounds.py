import json

import pytest

from soundcloudopen.xunia_sounds import (
    BEATSTARS_MCP_URL,
    MODE,
    build_discovery_prompt,
    build_xunia_mission,
    main,
    render_connector_guide,
)


def test_builds_beatstars_claude_virginia_mission():
    mission = build_xunia_mission("dark melodic trap around 90 BPM")
    assert mission["mode"] == MODE
    assert mission["claude"]["mode"] == "3LM CLAUDE"
    assert mission["beatstars"]["endpoint"] == BEATSTARS_MCP_URL
    assert mission["virginia"]["steps"][0] == "DESCRIBE_SOUND"
    assert "PREVIEW_CANDIDATES_IN_CLAUDE" in mission["virginia"]["steps"]
    assert mission["soundcloud"] is None


def test_expands_intelligent_discovery_prompt():
    prompt = build_discovery_prompt(
        "cold melodic trap",
        bpm=92,
        genre="trap",
        mood="haunting",
        use_case="album single",
        count=4,
    )
    assert "Find 4 beats on BeatStars" in prompt
    assert "genre: trap" in prompt
    assert "mood: haunting" in prompt
    assert "around 92 BPM" in prompt
    assert "intended use: album single" in prompt
    assert "preview the matching beats in Claude" in prompt


def test_adds_discovery_filters_to_mission():
    mission = build_xunia_mission(
        "cinematic workout ad",
        bpm=140,
        genre="drill",
        mood="disciplined and dark",
        use_case="paid 30 second advertisement",
        count=3,
    )
    filters = mission["beatstars"]["filters"]
    assert filters == {
        "genre": "drill",
        "mood": "disciplined and dark",
        "bpm": 140,
        "useCase": "paid 30 second advertisement",
        "requestedResults": 3,
    }
    assert "REVIEW_PRODUCER_LICENSE" in mission["virginia"]["steps"]


def test_rejects_invalid_discovery_ranges():
    with pytest.raises(ValueError):
        build_discovery_prompt("trap", bpm=0)
    with pytest.raises(ValueError):
        build_discovery_prompt("trap", count=11)


def test_adds_authorized_soundcloud_source():
    url = "https://soundcloud.com/example/sets/owned-beats"
    mission = build_xunia_mission("find similar beats", soundcloud_url=url, audio_format="wav")
    assert mission["soundcloud"] == {
        "url": url,
        "role": "authorized-media-source",
        "audioFormat": "wav",
    }
    assert "IMPORT_AUTHORIZED_SOUNDCLOUD_MEDIA" in mission["virginia"]["steps"]


def test_rejects_non_soundcloud_source():
    with pytest.raises(ValueError):
        build_xunia_mission("find similar beats", soundcloud_url="https://example.com/file.mp3")


def test_connector_guide_contains_exact_beatstars_mcp_url():
    assert BEATSTARS_MCP_URL in render_connector_guide()


def test_cli_writes_json(tmp_path, capsys):
    destination = tmp_path / "mission.json"
    rc = main([
        "warm soul beat",
        "--genre",
        "soul",
        "--mood",
        "hopeful",
        "--bpm",
        "85",
        "--count",
        "5",
        "--json",
        str(destination),
    ])
    assert rc == 0
    saved = json.loads(destination.read_text(encoding="utf-8"))
    assert saved["beatstars"]["intent"] == "warm soul beat"
    assert saved["beatstars"]["filters"]["bpm"] == 85
    assert MODE in capsys.readouterr().out


def test_cli_prompt_only(capsys):
    rc = main(["minimal dark trap", "--bpm", "90", "--count", "2", "--prompt-only"])
    assert rc == 0
    output = capsys.readouterr().out
    assert "Find 2 beats on BeatStars" in output
    assert "around 90 BPM" in output
    assert MODE not in output
