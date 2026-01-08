from fastapi import FastAPI

app = FastAPI(title="ChatGPT Wrapped")


@app.get("/")
def root():
    return {"status": "running"}
