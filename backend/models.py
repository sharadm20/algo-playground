from pydantic import BaseModel

class RunRequest(BaseModel):
    code: str
    lang: str

class TestResult(BaseModel):
    name: str
    passed: bool
    expected: str
    actual: str

class RunResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    timing_ms: int
    tests: list[TestResult] | None = None

class LanguageInfo(BaseModel):
    lang: str
    available: bool
    version: str | None = None
