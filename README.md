<div align="center">

![SOUNDCLOUD OPEN command-center flow](docs/assets/command-center.svg)

# SOUNDCLOUD OPEN

**CREATOR-OWNED MEDIA WORKFLOW**

[![Sonoxo](https://img.shields.io/badge/SONOXO-ECOSYSTEM-7c3aed?style=for-the-badge)](https://github.com/sonoxo)
![Status](https://img.shields.io/badge/STATUS-WORKING%20CLI-111827?style=for-the-badge)
![XUNIA Sounds](https://img.shields.io/badge/XUNIA%20SOUNDS-3LM%20CLAUDE%20%2B%20BEATSTARS%20%2B%20VIRGINIA-8d6bff?style=for-the-badge)

</div>

## What it does

SoundCloudOpen is a cross-platform Python command-line frontend for `yt-dlp`. It organizes permitted SoundCloud tracks or playlists with artwork and available metadata.

> Use it only for audio you own, downloads SoundCloud permits, or material you otherwise have permission to save. It does not bypass DRM or account permissions.

# XUNIA SOUNDS — beginner version

![XUNIA SOUNDS beginner function map](docs/assets/xunia-sounds-flow.svg)

**You describe the sound → VIRGINIA expands the idea → 3LM CLAUDE uses the BeatStars MCP connector → BeatStars intelligent search finds matches → you preview and compare them → you open the beat on BeatStars → you review the producer's license → SoundCloudOpen can optionally organize SoundCloud media you are allowed to save → XUNIA SOUNDS gives you one JSON workflow record.**

That integration is additive. It does not replace the original SoundCloud downloader.

### First-time BeatStars / Claude setup

After installing SoundCloudOpen, run:

```bash
xunia-sounds --claude-setup
```

It prints the beginner connector setup for Claude using:

```text
https://mcp.beatstars.com/mcp
```

Claude handles connector authentication and permissions. SoundCloudOpen does not ask for or store your BeatStars password.

### Ask for a sound

```bash
xunia-sounds "dark melodic trap with cold synths"
```

XUNIA SOUNDS returns a VIRGINIA-style mission that keeps the roles easy to understand:

| Part | Beginner meaning | Job |
|---|---|---|
| **You** | The creative director | Describe the sound you want |
| **VIRGINIA** | The plan | Expand the idea into clear discovery + review steps |
| **3LM CLAUDE** | The tool operator | Use the BeatStars connector in the conversation |
| **BeatStars MCP** | The BeatStars doorway | Expose the tools BeatStars makes available at connection time |
| **BeatStars** | Intelligent discovery + licensing destination | Find candidates, preview them, then open the full beat page |
| **SoundCloudOpen** | Your local media organizer | Handle SoundCloud media you own or are allowed to save |
| **XUNIA SOUNDS JSON** | The receipt | Record the requested workflow, filters, and evidence state |

### Make BeatStars discovery precise without learning search syntax

```bash
xunia-sounds \
  "cold melodic trap with space for vocals" \
  --genre trap \
  --mood "haunting but confident" \
  --bpm 92 \
  --use-case "album single" \
  --count 5
```

Those controls become one natural-language BeatStars discovery request. XUNIA SOUNDS asks the connected workflow to return candidates, explain why they fit, preview them in Claude when supported, and hand the selected result back to BeatStars for full listening and license review.

For a copy/paste-ready Claude request only:

```bash
xunia-sounds \
  "warm live-feeling drums and dusty keys" \
  --genre "soulful hip-hop" \
  --mood "melancholy but hopeful" \
  --bpm 85 \
  --count 5 \
  --prompt-only
```

### Combine BeatStars discovery with an authorized SoundCloud source

```bash
xunia-sounds \
  "find beats with a similar dark melodic atmosphere" \
  --soundcloud "https://soundcloud.com/example/sets/my-owned-catalog" \
  --format wav \
  --json xunia-mission.json
```

The SoundCloud URL is checked by the same validation already used by SoundCloudOpen. The generated mission labels it as an `authorized-media-source`.

> XUNIA SOUNDS does **not** invent a private BeatStars upload API. The BeatStars connector is treated as a remote MCP tool provider, and Claude discovers the tools BeatStars actually exposes. Producers control their own license terms, so licensing remains a BeatStars review step.

Full beginner guide: [XUNIA SOUNDS / 3LM CLAUDE / BEATSTARS / VIRGINIA](docs/XUNIA_SOUNDS.md)

## The original SoundCloud four-step flow

1. Give the CLI an authorized SoundCloud URL.
2. SoundCloudOpen builds the `yt-dlp` job and can use your own browser session for content you may access.
3. FFmpeg converts audio and embeds available artwork and metadata.
4. Numbered tracks and separate JPG covers land in an organized playlist folder.

## Quick start

```bash
git clone https://github.com/sonoxo/soundcloudopen.git
cd soundcloudopen
python3 -m pip install .
soundcloudopen --check
soundcloudopen --browser chrome "PLAYLIST_URL"
```

Install FFmpeg separately. Use `--browser none` for public content without browser-cookie access.

## Useful commands

```bash
soundcloudopen --list "PLAYLIST_URL"
soundcloudopen --save-json "PLAYLIST_URL"
soundcloudopen --format m4a "PLAYLIST_URL"
sco --check
xunia-sounds --claude-setup
xunia-sounds "warm soulful beat" --bpm 85 --mood hopeful --count 5
xunia-sounds "dark trap" --bpm 90 --count 3 --prompt-only
```

Supported output formats include MP3, M4A, FLAC, WAV, and Opus. Converting a lossy source to FLAC or WAV does not restore lost quality.

## Development

```bash
python3 -m pip install -e . pytest
pytest -q
```

CI targets macOS, Windows, Linux, Python 3.10, and Python 3.12. Docker support is included; host browser-cookie extraction is intended for native installs.

The XUNIA SOUNDS tests verify the BeatStars MCP endpoint, VIRGINIA/3LM CLAUDE mission structure, intelligent discovery prompt expansion, BPM/genre/mood/use-case controls, result-count validation, SoundCloud URL validation, prompt-only output, and JSON mission export.

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**SONOXO ECOSYSTEM** · Beginner first · Real functions · Creator-owned workflow

The header animation automatically becomes static when your system requests reduced motion.

</div>
