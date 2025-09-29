from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import logging
import os

app = FastAPI(title="Y.Nav API", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class AnalysisRequest(BaseModel):
    text: str
    context: str = "technical project communication"

class AnalysisResponse(BaseModel):
    analysis: str
    risk_level: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Y.Nav API"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_communication(request: AnalysisRequest):
    try:
        prompt = f"""
        Analyze this technical communication:
        
        Context: {request.context}
        Text: {request.text}
        
        Provide your analysis in the specified format.
        """
        
        result = subprocess.run(
            ["ollama", "run", "y-nav", prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Ollama error: {result.stderr}")
        
        response_text = result.stdout.strip()
        
        # Simple risk level extraction (you can improve this)
        risk_level = "Medium"
        if "high" in response_text.lower() or "critical" in response_text.lower():
            risk_level = "High"
        elif "low" in response_text.lower():
            risk_level = "Low"
        
        return AnalysisResponse(
            analysis=response_text,
            risk_level=risk_level
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Analysis timeout")
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: AnalysisRequest):
    try:
        result = subprocess.run(
            ["ollama", "run", "y-nav", request.text],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Ollama error: {result.stderr}")
        
        return {"response": result.stdout.strip()}
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Chat timeout")
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
