import json
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from uplc.app import state
from lib.llm import LLM
from ocr import perform_ocr

llm = LLM()

app = FastAPI(title="Simple Health Check API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def health_check():
    return {"status": "ok", "service": "fastapi-health-check"}

@app.get("/")
def read_root():
    return state()


@app.get("/ask/{question}" )
def ask(question : str):
    response = llm.ask(question)
    return {"response" : response}


@app.post("/extract-table")
async def extract_table(file: UploadFile = File(...)):
    image_bytes = await file.read()
    mime_type = file.content_type or "image/jpeg"
    
    try:
        json_response = llm.extract_table_data(image_bytes, mime_type)
        return json.loads(json_response)
    except Exception as e:
        return {"error": str(e)}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    mime_type = file.content_type or "image/jpeg"
    
    try:
        json_response = perform_ocr(image_bytes, mime_type)
        return json.loads(json_response)
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)  