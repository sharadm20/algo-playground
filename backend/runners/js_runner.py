import shutil
from .base import BaseRunner
from sandbox import Sandbox
from models import RunResponse

class JsRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as sb:
            filepath = f"{sb.temp_dir}/script.js"
            with open(filepath, "w") as f:
                f.write(code)
            result = sb.run(["node", filepath], sb.temp_dir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("node") is not None
