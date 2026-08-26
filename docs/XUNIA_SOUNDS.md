# XUNIA SOUNDS // 3LM CLAUDE // BEATSTARS // VIRGINIA

![XUNIA SOUNDS function map](assets/xunia-sounds-flow.svg)

## Beginner version

XUNIA SOUNDS gives the SoundCloudOpen project a second lane:

**You describe the sound → VIRGINIA expands the idea into a precise discovery request → Claude uses the BeatStars MCP connector → BeatStars intelligent search returns matching beats → you preview and compare them in Claude → you open the selected beat on BeatStars → you review the producer's current license → SoundCloudOpen can optionally organize SoundCloud media you are allowed to save → XUNIA SOUNDS records the workflow as JSON.**

It is intentionally split this way so each platform does the job it actually supports.

## What is implemented

The package installs two XUNIA SOUNDS commands:

```bash
xunia-sounds
xuniasounds
```

They both run the same VIRGINIA mission builder.

### 1. Connect BeatStars to Claude

```bash
xunia-sounds --claude-setup
```

The command prints the beginner setup using the BeatStars remote MCP endpoint:

```text
https://mcp.beatstars.com/mcp
```

Claude performs the connector authentication/permission flow. SoundCloudOpen does not collect or store the BeatStars password.

### 2. Describe the beat you want

```bash
xunia-sounds "dark melodic trap with cold synths"
```

XUNIA SOUNDS creates an expanded natural-language discovery prompt designed for the BeatStars Claude workflow.

You can make the request much more precise without learning BeatStars search syntax:

```bash
xunia-sounds \
  "cold melodic trap with space for vocals" \
  --genre trap \
  --mood "haunting but confident" \
  --bpm 92 \
  --use-case "album single" \
  --count 5
```

The generated mission records those values as explicit BeatStars discovery filters and asks Claude to:

1. send the natural-language creative direction to the BeatStars connector;
2. return matching BeatStars candidates;
3. let you preview the matches inside Claude when the connector provides previews;
4. explain why each candidate fits;
5. hand the selected result back to its BeatStars page; and
6. keep the license state at **review required** until you inspect the producer's current terms.

### 3. Copy only the Claude discovery prompt

```bash
xunia-sounds \
  "warm live-feeling drums and dusty keys" \
  --genre "soulful hip-hop" \
  --mood "melancholy but hopeful" \
  --bpm 85 \
  --count 5 \
  --prompt-only
```

This prints only the expanded BeatStars natural-language request so a beginner can paste it directly into a Claude conversation with the BeatStars connector enabled.

### 4. Add an authorized SoundCloud source when useful

```bash
xunia-sounds \
  "find beats with a similar dark melodic atmosphere" \
  --soundcloud "https://soundcloud.com/example/sets/my-owned-catalog" \
  --format wav \
  --json xunia-mission.json
```

The SoundCloud URL is validated using SoundCloudOpen's existing URL validation. It is included as an `authorized-media-source` in the mission.

## Mission shape

The generated JSON separates the systems clearly:

```text
mode
├── VIRGINIA creative intent
├── expanded BeatStars natural-language search prompt
├── requested BPM / genre / mood / use case / result count
├── 3LM CLAUDE orchestration role
├── BeatStars remote MCP endpoint + intelligent discovery workflow
├── license-review-required handoff
├── optional authorized SoundCloud source
└── evidence / guardrails
```

The BeatStars tools themselves are discovered by Claude from the BeatStars MCP server at connection time. This repo does not hard-code undocumented BeatStars private API calls.

## Why the BeatStars side is discovery-first

BeatStars publicly describes its Claude integration as a natural-language beat-discovery workflow. The user describes vibe, energy, genre, style, BPM, or a creative scenario; the BeatStars integration can return matching results for preview in Claude, and the user can open a result on BeatStars to hear the full beat and review licensing.

XUNIA SOUNDS mirrors that actual flow instead of inventing unsupported BeatStars endpoints.

For licensing, the selected beat is handed back to BeatStars because producers control their own license terms, pricing, and usage conditions. XUNIA SOUNDS therefore records licensing as a review step rather than assuming that a specific license applies.

This project does **not** claim BeatStars MCP is an upload API. BeatStars' creator documentation still describes uploads through BeatStars Studio, so XUNIA SOUNDS does not invent unsupported publishing endpoints.

## Discovery validation

XUNIA SOUNDS validates the structured discovery controls before it builds a mission:

- BPM must be between `1` and `400`.
- Requested BeatStars candidates must be between `1` and `10`.
- Empty genre, mood, and use-case values are normalized away.
- Optional SoundCloud references must still be valid SoundCloud URLs.

## SoundCloud side

The original SoundCloudOpen downloader remains intact. Use it only for:

- audio you own;
- downloads SoundCloud permits; or
- material you otherwise have permission to save.

XUNIA SOUNDS does not change or bypass SoundCloud permissions.

## Development

Run the full test suite:

```bash
python3 -m pip install -e . pytest
pytest -q
```

The XUNIA SOUNDS tests verify:

- the exact BeatStars MCP URL;
- 3LM CLAUDE + VIRGINIA mission structure;
- intelligent discovery prompt expansion;
- BPM / genre / mood / use-case / result-count controls;
- preview and producer-license-review workflow steps;
- optional SoundCloud URL validation;
- prompt-only output;
- JSON mission export; and
- rejection of invalid discovery ranges and non-SoundCloud URLs.

## Public references used for this implementation

- BeatStars Claude entry point: `https://www.beatstars.com/claude`
- BeatStars remote MCP endpoint: `https://mcp.beatstars.com/mcp`
- BeatStars search guidance: `https://help.beatstars.com/hc/en-us/articles/206702787-How-do-I-search-for-beats`
- BeatStars license guidance: `https://help.beatstars.com/hc/en-us/articles/360047401174-What-if-I-have-a-question-about-a-license-product-or-service-purchase`
- BeatStars upload guidance: `https://help.beatstars.com/hc/en-us/articles/1260802609630-How-Do-I-Upload-Tracks`
