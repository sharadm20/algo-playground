import shutil
import re
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import TestResult

class PythonRunner(BaseRunner):
    def execute(self, code: str):
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/script.py"
            with open(filepath, "w") as f:
                f.write(code)
            result = self.sandbox.run(["python", filepath], tmpdir)
            tests = self.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("python") is not None

    @staticmethod
    def parse_tests(output: str):
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
