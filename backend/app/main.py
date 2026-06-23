from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.grants import router as grants_router
from app.api.match import router as match_router

app = FastAPI(title="UK Farm Grant Matcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grants_router)
app.include_router(match_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
