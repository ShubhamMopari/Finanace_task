from fastapi import FastAPI
from app.routes.grants import router

app = FastAPI(title="Document Access Grant Service")

app.include_router(router)

@app.get("/")
async def health():
    return {"status": "running"}
