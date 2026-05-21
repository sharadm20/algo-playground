from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from runners import RUNNERS
from models import RunRequest, RunResponse, LanguageInfo

app = FastAPI(title="DSA Code Runner")

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
