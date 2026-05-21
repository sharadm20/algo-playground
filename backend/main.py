from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from runners import RUNNERS
from models import RunRequest, RunResponse, LanguageInfo

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
