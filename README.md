# Audio Transcription Tool

A Python script that transcribes meeting audio files using OpenAI's Whisper API and automatically generates concise meeting notes using GPT-4o. Two plain-text files are produced for every run: the full transcript and structured meeting notes.

## Features

- Transcribe audio files using OpenAI's Whisper model
- Automatically generate structured meeting notes (summary, key points, decisions, action items) via GPT-4o
- Outputs two plain-text files per run — transcript and notes
- Includes transcription date/time in each file
- Optional timestamp support to track when each segment was spoken
- Supports multiple audio formats (m4a, mp3, wav, etc.)
- Secure API key management using environment variables

## Prerequisites

- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/onucharles/audio-transcribe.git
   cd audio-transcribe
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**

   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY='your-api-key-here'" > .env
   ```

   Or export it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

### Basic Usage

Transcribe an audio file and generate meeting notes (saves to `output/YYYYMMDD_HHMMSS_transcript.txt` and `output/YYYYMMDD_HHMMSS_notes.txt`):
```bash
python transcribe.py meeting.m4a
```

### Custom Output Base Name

Specify a base name for the two output files:
```bash
python transcribe.py meeting.m4a -o my-meeting
# writes: my-meeting_transcript.txt and my-meeting_notes.txt
```

### Include Timestamps

Add timestamps for each spoken segment in the transcript:
```bash
python transcribe.py meeting.m4a --timestamps
```

### Command Line Options

```
usage: transcribe.py [-h] [-o OUTPUT] [--timestamps] audio_file

positional arguments:
  audio_file            Path to the audio file to transcribe

optional arguments:
  -h, --help            Show help message and exit
  -o OUTPUT, --output OUTPUT
                        Base name for output files (optional).
                        Writes <base>_transcript.txt and <base>_notes.txt.
                        Defaults to output/YYYYMMDD_HHMMSS
  --timestamps          Include timestamps in the transcript output
```

## Output Files

Each run produces two files in the `output/` directory (or at a custom path):

**`YYYYMMDD_HHMMSS_transcript.txt`** — full verbatim transcript:
```
Meeting Transcript
Transcribed on: March 03, 2026 at 05:00 PM
------------------------------------------------------------

[full transcript text]
```

**`YYYYMMDD_HHMMSS_notes.txt`** — AI-generated meeting notes:
```
Meeting Notes
Transcribed on: March 03, 2026 at 05:00 PM
------------------------------------------------------------

Summary
...

Key Discussion Points
- ...

Decisions Made
- ...

Action Items
- ...
```

## File Structure

```
audio-transcribe/
├── transcribe.py      # Main script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (API key) - create this
├── .gitignore        # Git ignore rules
├── output/           # Output directory for transcripts and notes (auto-created)
└── README.md         # This file
```

## How It Works

1. **Input**: The script accepts an audio file path as input
2. **Transcription**: The audio is sent to OpenAI's Whisper API, which returns the transcribed text with optional segment timestamps
3. **Transcript file**: The raw transcript is written to `*_transcript.txt`
4. **Notes generation**: The transcript is sent to GPT-4o, which produces structured meeting notes covering the summary, key discussion points, decisions made, and action items
5. **Notes file**: The meeting notes are written to `*_notes.txt`

## Supported Audio Formats

The OpenAI Whisper API supports: M4A, MP3, MP4, MPEG, MPGA, WAV, WEBM

Maximum file size: 25 MB

## API Costs

- **Whisper**: $0.006 per minute of audio
- **GPT-4o**: charged per token (input + output) — see [OpenAI's pricing page](https://openai.com/api/pricing/) for current rates

## Error Handling

- **File not found**: Checks if the audio file exists before processing
- **Missing API key**: Validates that `OPENAI_API_KEY` is set
- **API errors**: Catches and reports transcription or notes generation failures

## Development Notes

The script uses:
- `openai` — Whisper transcription and GPT-4o notes generation
- `python-dotenv` — environment variable management
- `argparse` — command-line argument parsing
- `pathlib` — cross-platform file path handling

## License

This is a personal utility script. Use it as you wish!

## Quick Reference

```bash
# Basic usage (saves to output/YYYYMMDD_HHMMSS_transcript.txt and _notes.txt)
python transcribe.py meeting.m4a

# Custom base name for output files
python transcribe.py meeting.m4a -o my-meeting

# With timestamps in transcript
python transcribe.py meeting.m4a --timestamps

# Set API key (if not in .env)
export OPENAI_API_KEY='sk-...'
```
