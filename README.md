# Audio Transcription Tool

A simple Python script that transcribes audio files to text using OpenAI's Whisper API. Supports various audio formats including M4A, MP3, WAV, and more.

## Features

- 🎯 Transcribe audio files to text using OpenAI's state-of-the-art Whisper model
- 📝 Save transcriptions to a text file or print to console
- ⏱️ Optional timestamp support to track when each segment was spoken
- 🎵 Supports multiple audio formats (m4a, mp3, wav, etc.)
- 🔐 Secure API key management using environment variables

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

Transcribe an audio file and print to console:
```bash
python transcribe.py my-audio.m4a
```

### Save to File

Save transcription to a text file:
```bash
python transcribe.py my-audio.m4a -o output.txt
```

### Include Timestamps

Get transcription with timestamps for each segment:
```bash
python transcribe.py my-audio.m4a --timestamps
```

Or save timestamped transcription to file:
```bash
python transcribe.py my-audio.m4a --timestamps -o output.txt
```

### Command Line Options

```
usage: transcribe.py [-h] [-o OUTPUT] [--timestamps] audio_file

positional arguments:
  audio_file            Path to the audio file to transcribe

optional arguments:
  -h, --help            Show help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (optional, prints to stdout if not specified)
  --timestamps          Include timestamps in output
```

## File Structure

```
audio-transcribe/
├── transcribe.py      # Main transcription script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (API key) - create this
├── my-audio.m4a      # Example audio file
├── output.txt        # Example output file
└── README.md         # This file
```

## How It Works

1. **Input**: The script accepts an audio file path as input
2. **Processing**: It reads the audio file and sends it to OpenAI's Whisper API
3. **Response**: The API returns the transcribed text with optional segment timestamps
4. **Output**: Results are either printed to console or saved to a specified file

## Supported Audio Formats

The OpenAI Whisper API supports:
- M4A
- MP3
- MP4
- MPEG
- MPGA
- WAV
- WEBM

Maximum file size: 25 MB

## Error Handling

The script handles common errors:
- **File not found**: Checks if the audio file exists before processing
- **Missing API key**: Validates that OPENAI_API_KEY is set
- **API errors**: Catches and reports transcription failures

## Example Output

**Without timestamps:**
```
This is an example transcription of the audio file. The text flows naturally without any time markers.
```

**With timestamps:**
```
[0.00s - 3.45s] This is an example transcription
[3.45s - 7.20s] of the audio file with timestamps
[7.20s - 10.15s] showing when each segment was spoken.
```

## API Costs

This tool uses OpenAI's Whisper API which charges $0.006 per minute of audio. Check [OpenAI's pricing page](https://openai.com/api/pricing/) for current rates.

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"
Make sure you've created a `.env` file with your API key or exported it as an environment variable.

### "Audio file not found"
Check that the path to your audio file is correct. Use absolute paths if relative paths aren't working.

### "File size too large"
The Whisper API has a 25 MB file size limit. Compress or split your audio file if it exceeds this limit.

## Development Notes

The script uses:
- `openai` library for API interactions
- `python-dotenv` for environment variable management
- `argparse` for command-line argument parsing
- `pathlib` for cross-platform file path handling

## License

This is a personal utility script. Use it as you wish!

## Quick Reference

```bash
# Basic transcription
python transcribe.py audio.m4a

# Save to file
python transcribe.py audio.m4a -o output.txt

# With timestamps
python transcribe.py audio.m4a --timestamps -o output.txt

# Set API key (if not in .env)
export OPENAI_API_KEY='sk-...'
```
