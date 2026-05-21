import shutil
from models import RunResponse
from .base import BaseRunner

class PythonRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with self.sandbox as sb:
            filepath = f"{sb.temp_dir}/script.py"
            with open(filepath, "w") as f:
                f.write(code)
            result = sb.run(["python", filepath], sb.temp_dir)
            tests = BaseRunner.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("python") is not None

