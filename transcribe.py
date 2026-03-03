"""
Audio Transcription Script
Transcribes M4A (and other audio formats) to text using OpenAI's Whisper API.
Outputs a plain-text transcript and AI-generated meeting notes.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def write_transcript_txt(output_path: Path, text: str, transcription_date: str):
    """
    Write the raw transcript to a plain-text file.

    Args:
        output_path: Path where the transcript should be saved
        text: The transcription text
        transcription_date: The date/time when transcription was performed
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Meeting Transcript\n")
        f.write(f"Transcribed on: {transcription_date}\n")
        f.write("-" * 60 + "\n\n")
        f.write(text)
        f.write("\n")


def generate_meeting_notes(client: OpenAI, transcript_text: str) -> str:
    """
    Generate concise meeting notes from a transcript using GPT-4o.

    Args:
        client: An initialised OpenAI client
        transcript_text: The full transcript text

    Returns:
        A structured meeting notes string.
    """
    print("Generating meeting notes...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert meeting note-taker. "
                    "Given a meeting transcript, produce concise, well-structured meeting notes. "
                    "Your notes must include the following sections:\n\n"
                    "1. Summary — a short paragraph capturing the overall purpose and outcome of the meeting.\n"
                    "2. Key Discussion Points — bullet list of the main topics discussed.\n"
                    "3. Decisions Made — bullet list of any decisions or agreements reached.\n"
                    "4. Action Items — bullet list of tasks, owners (if mentioned), and deadlines (if mentioned).\n\n"
                    "Be concise. Do not reproduce the transcript verbatim. "
                    "If a section has nothing to report, write 'None noted.'"
                ),
            },
            {
                "role": "user",
                "content": f"Here is the meeting transcript:\n\n{transcript_text}",
            },
        ],
    )
    return response.choices[0].message.content.strip()


def write_notes_txt(output_path: Path, notes: str, transcription_date: str):
    """
    Write the AI-generated meeting notes to a plain-text file.

    Args:
        output_path: Path where the notes should be saved
        notes: The meeting notes text
        transcription_date: The date/time when transcription was performed
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Meeting Notes\n")
        f.write(f"Transcribed on: {transcription_date}\n")
        f.write("-" * 60 + "\n\n")
        f.write(notes)
        f.write("\n")


def transcribe_audio(audio_path: str) -> dict:
    """
    Load an audio file and transcribe it using OpenAI's Whisper API.

    Args:
        audio_path: Path to the audio file (m4a, mp3, wav, etc.)

    Returns:
        Dictionary containing transcription result with 'text' and 'segments' keys.
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
        ],
        "client": client,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files (m4a, mp3, wav, etc.) and generate meeting notes using OpenAI"
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to transcribe"
    )
    parser.add_argument(
        "-o", "--output",
        help=(
            "Base name for output files (optional). "
            "Two files will be written: <base>_transcript.txt and <base>_notes.txt. "
            "Defaults to output/YYYYMMDD_HHMMSS"
        )
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in the transcript output"
    )

    args = parser.parse_args()

    transcription_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        result = transcribe_audio(args.audio_file)
        client = result["client"]

        # Format transcript text
        if args.timestamps:
            output_lines = []
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                output_lines.append(f"[{start:.2f}s - {end:.2f}s] {text}")
            transcript_text = "\n".join(output_lines)
        else:
            transcript_text = result["text"].strip()

        # Determine output base path
        if args.output:
            base = Path(args.output)
        else:
            base = Path("output") / timestamp

        transcript_path = base.parent / f"{base.name}_transcript.txt"
        notes_path = base.parent / f"{base.name}_notes.txt"

        # Write transcript
        write_transcript_txt(transcript_path, transcript_text, transcription_date)
        print(f"Transcript saved to: {transcript_path}")

        # Generate and write meeting notes
        notes = generate_meeting_notes(client, transcript_text)
        write_notes_txt(notes_path, notes, transcription_date)
        print(f"Meeting notes saved to: {notes_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
