from fastapi import requests
from fastapi import FastAPI
from uplc.app import state
from lib.llm import LLM

llm = LLM()

app = FastAPI(title="Simple Health Check API")

def health_check():
    return {"status": "ok", "service": "fastapi-health-check"}

@app.get("/")
def read_root():
    return state()


@app.get("/ask/{question}" )
def ask(question : str):
    response = llm.ask(question)
    return {"response" : response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)  