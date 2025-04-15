import asyncio

import uvicorn
from fastapi import FastAPI, UploadFile, File

from data_preparator.resume_reader import ResumeReader
from llm.model import Model

app = FastAPI()

@app.post('/predict')
async def predict(request: str, file: UploadFile = File(...)):
    # with open(file.filename, "wb") as f:
    #     while chunk := await file.read(1024):
    #         f.write(chunk)

    resume = ResumeReader(file.filename)
    model = Model(model_name="gemma3:1b", request=request, resume=resume.extract_text())
    result = await model.response()
    return result
