import shutil
import os
import re
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import TestResult

class RustRunner(BaseRunner):
    TEMPLATE = """fn main() {{
    {}
}}"""

    def execute(self, code: str):
        wrapped = self.TEMPLATE.format(code) if "fn main" not in code else code
        with Sandbox() as tmpdir:
            src_dir = f"{tmpdir}/src"
            os.makedirs(src_dir, exist_ok=True)
            with open(f"{src_dir}/main.rs", "w") as f:
                f.write(wrapped)
            with open(f"{tmpdir}/Cargo.toml", "w") as f:
                f.write('[package]\nname = "temp"\nversion = "0.1.0"\nedition = "2021"\n')
            result = self.sandbox.run(["cargo", "run", "-q"], tmpdir)
            tests = self.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("rustc") is not None

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
