from fastapi import FastAPI

app = FastAPI(title="Clube de Xadrez API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Clube de Xadrez Backend"}
