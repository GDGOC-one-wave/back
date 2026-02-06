from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from .ai_service import AIService

app = FastAPI(title="Startup Mate AI Backend")

# 요청 스키마 정의
class ProjectData(BaseModel):
    formData: Dict[str, str]
    currentStep: int

class QuestionRequest(BaseModel):
    fieldId: str
    nextLabel: str
    formData: Dict[str, str]

@app.get("/")
def read_root():
    return {"message": "Startup Mate AI API is running"}

@app.post("/api/verify-phase1")
async def verify_phase1(data: ProjectData):
    try:
        # 1-1~1-3, 2-1~2-3 데이터 분리 (예시)
        step1 = {k: v for k, v in data.formData.items() if k.startswith("1-")}
        step2 = {k: v for k, v in data.formData.items() if k.startswith("2-")}
        result = AIService.verify_phase1(step1, step2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
async def simulate_bm(data: ProjectData):
    try:
        result = AIService.simulate_bm(data.formData)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/guided-questions")
async def guided_questions(req: QuestionRequest):
    try:
        questions = AIService.get_guided_questions(req.fieldId, req.nextLabel, req.formData)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_mentor(data: Dict[str, Any]):
    try:
        # data: { step, formData, message }
        answer = AIService.chat_with_mentor(
            data.get("step", 1), 
            data.get("formData", {}), 
            data.get("message", "")
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
