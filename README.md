# SoundCloudOpen

SoundCloudOpen is a free, open-source, cross-platform command-line frontend for `yt-dlp` that bulk-downloads SoundCloud playlists/tracks together with artwork and metadata.

> Use SoundCloudOpen only for audio you own, content SoundCloud explicitly permits you to download, or content you otherwise have permission to save. It does not bypass SoundCloud account permissions or DRM.

## What it does

The default download mirrors the working workflow:

- downloads the whole playlist
- continues past individual failures
- resumes interrupted downloads
- does not overwrite completed files
- saves separate JPG artwork for every track
- embeds artwork into the audio file
- embeds available metadata
- converts audio to high-quality MP3 by default
- numbers files in playlist order
- supports authenticated/private playlists by reading cookies from your own browser session

Output:

```text
~/Music/SoundCloud/
└── Playlist Name/
    ├── 001 - Artist - Track.mp3
    ├── 002 - Artist - Track.mp3
    └── Artwork/
        ├── 001 - Artist - Track.jpg
        └── 002 - Artist - Track.jpg
```

## Platforms

CI tests the project on:

- macOS
- Windows
- Linux
- Python 3.10 and 3.12

Docker is also supported.

Browsers supported for authenticated cookies include Chrome, Chromium, Firefox, Edge, Brave, Opera, Vivaldi, and Safari where supported by yt-dlp.

## Get SoundCloudOpen

Clone the public repository:

```bash
git clone https://github.com/sonoxo/soundcloudopen.git
cd soundcloudopen
```

### macOS / Linux

```bash
bash scripts/install.sh
```

Or manually:

```bash
python3 -m pip install .
```

FFmpeg must be installed. On macOS:

```bash
brew install ffmpeg
```

### Windows

From PowerShell:

```powershell
git clone https://github.com/sonoxo/soundcloudopen.git
cd soundcloudopen
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

## Check the setup

```bash
soundcloudopen --check
```

Short alias:

```bash
sco --check
```

## Download a playlist

```bash
soundcloudopen "https://soundcloud.com/USERNAME/sets/PLAYLIST"
```

For a private playlist visible in Chrome:

```bash
soundcloudopen --browser chrome "https://soundcloud.com/USERNAME/sets/PLAYLIST"
```

Browser auto-detection is enabled by default:

```bash
soundcloudopen "https://soundcloud.com/USERNAME/sets/PLAYLIST"
```

For a public playlist with no browser-cookie access:

```bash
soundcloudopen --browser none "https://soundcloud.com/USERNAME/sets/PLAYLIST"
```

## Working example

```bash
soundcloudopen --browser chrome "https://soundcloud.com/almightysonoxo/sets/all-songs"
```

## Choose another output folder

macOS/Linux:

```bash
soundcloudopen -o "$HOME/Desktop/SoundCloud" "PLAYLIST_URL"
```

Windows PowerShell:

```powershell
soundcloudopen -o "$HOME\Desktop\SoundCloud" "PLAYLIST_URL"
```

## Other audio formats

```bash
soundcloudopen --format m4a "PLAYLIST_URL"
soundcloudopen --format flac "PLAYLIST_URL"
soundcloudopen --format wav "PLAYLIST_URL"
soundcloudopen --format opus "PLAYLIST_URL"
```

Note: converting a lossy SoundCloud source to FLAC/WAV does not increase original source quality.

## Save metadata JSON too

```bash
soundcloudopen --save-json "PLAYLIST_URL"
```

## List tracks without downloading

```bash
soundcloudopen --list "PLAYLIST_URL"
```

## See the exact yt-dlp command

```bash
soundcloudopen --print-command --browser chrome "PLAYLIST_URL"
```

## Docker

Build:

```bash
docker build -t soundcloudopen .
```

Public playlist example:

```bash
docker run --rm -v "$HOME/Music/SoundCloud:/root/Music/SoundCloud" soundcloudopen --browser none "PLAYLIST_URL"
```

Browser cookie extraction is intended for native installs because host-browser cookie databases are not automatically available inside a container.

## Under the hood

The core download intentionally maps to these yt-dlp options:

```text
--yes-playlist
--ignore-errors
--continue
--no-overwrites
--write-thumbnail
--convert-thumbnails jpg
--embed-thumbnail
--embed-metadata
--extract-audio
--audio-format mp3
--audio-quality 0
```

Authenticated playlists add:

```text
--cookies-from-browser <browser>
```

## Development

```bash
python3 -m pip install -e . pytest
pytest -q
```

## License

MIT
