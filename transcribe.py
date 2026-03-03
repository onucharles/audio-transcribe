"""
Audio Transcription Script
Transcribes M4A (and other audio formats) to text using OpenAI's Whisper API.
Outputs transcriptions to PDF files with date headers.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

load_dotenv()


def generate_pdf(output_path: Path, transcription_text: str, transcription_date: str):
    """
    Generate a PDF file with the transcription.
    
    Args:
        output_path: Path where the PDF should be saved
        transcription_text: The transcription text to include
        transcription_date: The date/time when transcription was performed
    """
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container for PDF elements
    story = []
    styles = getSampleStyleSheet()
    
    # Add custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#2c3e50',
        spaceAfter=6
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#7f8c8d',
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )
    
    # Add title
    story.append(Paragraph("Audio Transcription", title_style))
    
    # Add date
    story.append(Paragraph(f"Transcribed on: {transcription_date}", date_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Add transcription text (handle line breaks)
    for paragraph in transcription_text.split('\n'):
        if paragraph.strip():
            # Escape special characters for reportlab
            safe_paragraph = paragraph.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(safe_paragraph, body_style))
    
    # Build PDF
    doc.build(story)


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
        description="Transcribe audio files (m4a, mp3, wav, etc.) to PDF using OpenAI API"
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to transcribe"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path (optional, defaults to output/transcription_YYYYMMDD_HHMMSS.pdf)"
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in output"
    )

    args = parser.parse_args()
    
    # Generate transcription date
    transcription_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    try:
        result = transcribe_audio(args.audio_file)

        # Format transcription text
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

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            # Default to output/ directory with timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path("output") / f"transcription_{timestamp}.pdf"
        
        # Ensure output has .pdf extension
        if output_path.suffix.lower() != '.pdf':
            output_path = output_path.with_suffix('.pdf')
        
        # Generate PDF
        generate_pdf(output_path, output_text, transcription_date)
        print(f"✓ Transcription saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
