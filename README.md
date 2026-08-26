<div align="center">

![SOUNDCLOUD OPEN command-center flow](docs/assets/command-center.svg)

# SOUNDCLOUD OPEN

**CREATOR-OWNED MEDIA WORKFLOW**

[![Sonoxo](https://img.shields.io/badge/SONOXO-ECOSYSTEM-7c3aed?style=for-the-badge)](https://github.com/sonoxo)
![Status](https://img.shields.io/badge/STATUS-WORKING%20CLI-111827?style=for-the-badge)

</div>

## What it does

SoundCloudOpen is a cross-platform Python command-line frontend for `yt-dlp`. It organizes permitted SoundCloud tracks or playlists with artwork and available metadata.

> Use it only for audio you own, downloads SoundCloud permits, or material you otherwise have permission to save. It does not bypass DRM or account permissions.

## The four-step flow

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
```

Supported output formats include MP3, M4A, FLAC, WAV, and Opus. Converting a lossy source to FLAC or WAV does not restore lost quality.

## Development

```bash
python3 -m pip install -e . pytest
pytest -q
```

CI targets macOS, Windows, Linux, Python 3.10, and Python 3.12. Docker support is included; host browser-cookie extraction is intended for native installs.

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**SONOXO ECOSYSTEM** · Built to make complex tools understandable

The header animation automatically becomes static when your system requests reduced motion.

</div>
