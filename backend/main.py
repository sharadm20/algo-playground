import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from runners import RUNNERS
from models import RunRequest, RunResponse, LanguageInfo, SolutionResponse

app = FastAPI(title="DSA Code Runner")

INTERNAL_HEADER = "X-Internal-Request"
INTERNAL_VALUE = "true"

@app.middleware("http")
async def restrict_direct_access(request: Request, call_next):
    if request.headers.get(INTERNAL_HEADER) != INTERNAL_VALUE:
        return JSONResponse(status_code=403, content={"detail": "Direct API access denied. Requests must go through the nginx proxy."})
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/languages", response_model=list[LanguageInfo])
def get_languages():
    result = []
    for lang, runner_cls in RUNNERS.items():
        runner = runner_cls()
        result.append(LanguageInfo(
            lang=lang,
            available=runner.detect(),
            version=None,
        ))
    return result

@app.post("/api/run", response_model=RunResponse)
def run_code(req: RunRequest):
    lang = req.lang.lower()
    if lang not in RUNNERS:
        raise HTTPException(400, f"Unsupported language: {lang}. Supported: {list(RUNNERS.keys())}")
    runner = RUNNERS[lang]()
    if not runner.detect():
        raise HTTPException(400, f"Runtime not found for {lang}. Install the toolchain and try again.")
    try:
        return runner.execute(req.code)
    except Exception as e:
        raise HTTPException(500, str(e))

CHALLENGES_INDEX_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "challenges", "index.json"))
CHALLENGES_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "challenges"))

def _load_challenge_index():
    with open(CHALLENGES_INDEX_PATH) as f:
        return json.load(f)

@app.get("/api/challenges")
def list_challenges():
    return _load_challenge_index()

@app.get("/api/challenges/{challenge_id}/solution", response_model=SolutionResponse)
def get_challenge_solution(challenge_id: str):
    index = _load_challenge_index()
    entry = next((c for c in index if c["id"] == challenge_id), None)
    if not entry:
        raise HTTPException(404, f"Challenge '{challenge_id}' not found")
    source_path = os.path.normpath(os.path.join(CHALLENGES_DIR, entry["sourcePath"]))
    if not source_path.startswith(CHALLENGES_DIR):
        raise HTTPException(404, "Invalid path")
    if not os.path.exists(source_path):
        raise HTTPException(404, "Solution file not found")
    with open(source_path) as f:
        code = f.read()
    return SolutionResponse(language=entry["language"], code=code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
