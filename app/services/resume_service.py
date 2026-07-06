from fastapi import UploadFile
from pathlib import Path
import aiofiles
import uuid

from sympy import content


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def save_resume(file: UploadFile):
    """
    Validate an uploaded resume and return basic information.
    """

    # Step 1: Make sure the file has a name
    if not file.filename:
        return {
            "success": False,
            "error": "No filename was provided."
        }

    # Step 2: Validate the file extension
    if not file.content_type in ALLOWED_TYPES:
        return {
            "success": False,
            "error": "Only PDF and DOCX files are allowed."
        }
        
    

    # Step 3: Read the uploaded file
    content = await file.read()

    ext = Path(file.filename).suffix.lower()
    safe_filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / safe_filename

    # Step 4: Save the file
    try:
        size = len(content)

        if size > MAX_FILE_SIZE:
            return {
                "success": False,
                "error": f"File too large (max {MAX_FILE_SIZE // 1024 // 1024} MB)"
            }

        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(content)

    except Exception as e:
        return {
            "success": False,
            "error": f"Error saving file: {e}"
        }

    finally:
        await file.close()

    return {
        "success": True,
        "original_filename": file.filename,
        "stored_filename": safe_filename,
        "content_type": file.content_type,
        "file_size": size,
        "saved_path": str(file_path)
    }