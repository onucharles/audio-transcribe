"""
Audio Transcription Script
Transcribes M4A (and other audio formats) to text using OpenAI's Whisper API.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def transcribe_audio(audio_path: str) -> dict:
    """
    Load an audio file and transcribe it using OpenAI's Whisper API.

    Args:
        audio_path: Path to the audio file (m4a, mp3, wav, etc.)

    Returns:
        Dictionary containing transcription result with 'text' key.
    """
    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Set it with: export OPENAI_API_KEY='your-key-here'"
        )

    client = OpenAI(api_key=api_key)

    print(f"Transcribing: {audio_file.name}")

    with open(audio_file, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json"
        )

    return {
        "text": response.text,
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in (response.segments or [])
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files (m4a, mp3, wav, etc.) to text using OpenAI API"
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to transcribe"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (optional, prints to stdout if not specified)"
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in output"
    )

    args = parser.parse_args()

    try:
        result = transcribe_audio(args.audio_file)

        if args.timestamps:
            output_lines = []
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                output_lines.append(f"[{start:.2f}s - {end:.2f}s] {text}")
            output_text = "\n".join(output_lines)
        else:
            output_text = result["text"].strip()

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output_text)
            print(f"Transcription saved to: {args.output}")
        else:
            print("\n--- Transcription ---\n")
            print(output_text)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
