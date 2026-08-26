import json

import pytest

from soundcloudopen.xunia_sounds import (
    BEATSTARS_MCP_URL,
    MODE,
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
    assert mission["soundcloud"] is None


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
    rc = main(["warm soul beat", "--json", str(destination)])
    assert rc == 0
    saved = json.loads(destination.read_text(encoding="utf-8"))
    assert saved["beatstars"]["intent"] == "warm soul beat"
    assert MODE in capsys.readouterr().out
