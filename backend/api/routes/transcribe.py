from fastapi import APIRouter, UploadFile, File, HTTPException
from services.groq_service import _get_client
import tempfile
import os

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio del candidato usando Whisper de Groq."""
    allowed_ext = ['mp3', 'wav', 'm4a', 'ogg', 'webm', 'mp4', 'mpeg', 'mpga']
    ext = file.filename.lower().split('.')[-1] if '.' in file.filename else 'webm'

    if ext not in allowed_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado. Usa: {', '.join(allowed_ext)}"
        )

    try:
        file_bytes = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        with open(tmp_path, 'rb') as audio_file:
            transcription = _get_client().audio.transcriptions.create(
                file=(file.filename, audio_file.read()),
                model="whisper-large-v3-turbo",
                response_format="text",
                language="es",
            )

        os.unlink(tmp_path)

        return {
            "transcription": transcription if isinstance(transcription, str) else str(transcription),
            "filename": file.filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribiendo: {str(e)}")