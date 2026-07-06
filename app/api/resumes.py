from fastapi import APIRouter, UploadFile
from app.services.resume_service import save_resume
from app.services.parser_service import parse_docx_resume
from app.services.ai_services import analyze_resume

router = APIRouter()

@router.post("/upload")
async def upload_resume(uploaded_file: UploadFile):

    # Step 1: Save the uploaded resume
    saved_resume = await save_resume(uploaded_file)

    # Step 2: Stop if saving failed
    if not saved_resume["success"]:
        return saved_resume

    # Step 3: Parse the saved resume
    extracted_text = parse_docx_resume(saved_resume["saved_path"])
    print(saved_resume)
    
    analysis = await analyze_resume(extracted_text)

    # Step 4: Return everything
    return {
        "resume": saved_resume,
        "text": extracted_text,
        "analysis": analysis
    }