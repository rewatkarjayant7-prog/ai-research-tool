import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.document_parser import extract_text
from backend.llm_service import analyze_transcript

app = FastAPI(title="AI Research Tool", description="Earnings Call / Management Commentary Summary Parser")

# Enable CORS (useful if frontend is ever hosted separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/api/analyze")
async def analyze_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")
    
    try:
        # Read file contents into memory
        contents = await file.read()
        
        # Parse text from file
        text = extract_text(contents, file.filename)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the document.")
            
        # Send to LLM
        summary = analyze_transcript(text)
        
        return JSONResponse(content=summary)
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Mount the static frontend directory
# Assuming 'frontend' directory is at the root alongside 'backend'
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the application from the project root using:
    # uvicorn backend.main:app --reload
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
