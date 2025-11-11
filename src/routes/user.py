from routes import prog
from routes.schemas import base
from helpers import llm_utils

import os
import glob
import shutil

from fastapi import HTTPException, UploadFile, File
from services import rag_pipeline


# API endpoint to upload a new PDF file
@prog.app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a new PDF file to use as a knowledge source"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        # Save the uploaded file
        source_name = os.path.splitext(file.filename)[0]
        file_path = f"data/{source_name}.pdf"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load the new knowledge source
        success, message = rag_pipeline.load_knowledge_source(source_name)

        return base.SourceResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


# API endpoint to get available sources
@prog.app.get("/sources", response_model=list)
async def get_available_sources():
    """Get list of available knowledge sources"""
    data_files = glob.glob("data/*.pdf")
    source_names = [os.path.basename(file).replace(".pdf", "") for file in data_files]
    return source_names


# API endpoint to select a knowledge source
@prog.app.post("/select_source")
async def select_source(source: base.SourceSelection):
    """Select a knowledge source to use for Q&A"""
    success, message = rag_pipeline.load_knowledge_source(source.source_name)
    return base.SourceResponse(success=success, message=message)


# API endpoint to submit an answer to the current question
@prog.app.post("/submit_answer")
async def submit_answer(request: base.AnswerRequest):
    """Submit an answer to the current interview question and get evaluation"""
    if not rag_pipeline.current_question:
        raise HTTPException(
            status_code=400,
            detail="No question available. Please generate a question first.",
        )

    try:
        # Generate a simple reference answer if needed
        if (
            rag_pipeline.reference_answer
            == "Reference answer will be generated after you submit your response."
        ):
            prompt = f"Short answer to: {rag_pipeline.current_question}"
            rag_pipeline.reference_answer = llm_utils.llm.invoke(prompt).content

        # Simple evaluation with concise feedback
        eval_prompt = f"Rate 0-10 and provide brief feedback (max 20 words): {request.answer} for question: {rag_pipeline.current_question}. Format as 'SCORE: X/10 FEEDBACK: [concise feedback]'"
        evaluation = llm_utils.llm.invoke(eval_prompt).content

        # Parse evaluation response
        if "SCORE:" in evaluation and "FEEDBACK:" in evaluation:
            parts = evaluation.split("FEEDBACK:")
            score = parts[0].replace("SCORE:", "").strip()
            feedback = parts[1].strip()

            return base.AnswerResponse(
                score=score,
                feedback=feedback,
                reference_answer=rag_pipeline.reference_answer,
                success=True,
                message="Answer evaluated successfully",
            )
        else:
            return base.AnswerResponse(
                score="N/A",
                feedback=evaluation,
                reference_answer=rag_pipeline.reference_answer,
                success=True,
                message="Answer evaluated successfully",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error evaluating answer: {str(e)}"
        )