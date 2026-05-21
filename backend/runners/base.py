import re
from abc import ABC, abstractmethod
from sandbox import Sandbox
from models import RunResponse, TestResult

class BaseRunner(ABC):
    def __init__(self):
        self.sandbox = Sandbox()

    @abstractmethod
    def execute(self, code: str) -> RunResponse:
        ...

    def detect(self) -> bool:
        return False

    @staticmethod
    def parse_tests(output: str) -> list[TestResult]:
        tests = []
        for line in output.split("\n"):
            m = re.match(r"(✅|❌|PASS|FAIL)\s*(.*)", line)
            if m:
                status = m.group(1) in ("✅", "PASS")
                tests.append(TestResult(
                    name=m.group(2).strip(),
                    passed=status,
                    expected="",
                    actual="",
                ))
        return tests

    def _make_response(self, result: dict, tests: list[TestResult] | None = None) -> RunResponse:
        return RunResponse(
            stdout=result["stdout"],
            stderr=result["stderr"],
            exit_code=result["exit_code"],
            timing_ms=result["timing_ms"],
            tests=tests or [],
        )
