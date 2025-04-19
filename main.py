import re

from fastapi import FastAPI, UploadFile, File

from data_preparator.resume_reader import ResumeReader
from db.database import DataBase
from llm.model import Model

app = FastAPI()

@app.post('/predict')
async def predict(request: str, name: str, file: UploadFile = File(...)):
    with open(file.filename, "wb") as f:
        while chunk := await file.read(1024):
            f.write(chunk)
    resume = ResumeReader(file.filename)
    model = Model(model_name="gemma3:1b", request=request, resume=resume.extract_text())
    result = await model.response()
    rating = "".join([re.search("[0-9]+", line).group() for line in result.splitlines() if "Rating" in line and len(re.findall("[0-9]+", line))>0])
    db = DataBase()
    db.connect_db("resumeai")
    db.insert_data("Candidates", name + ", " + rating, "Name, LastName, Positon, Rate")
    print(rating)
    return result
