import shutil
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import RunResponse

class JsRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        sb = Sandbox()
        tmpdir = sb.__enter__()
        try:
            filepath = f"{tmpdir}/script.js"
            with open(filepath, "w") as f:
                f.write(code)
            result = sb.run(["node", filepath], tmpdir)
            return self._make_response(result)
        finally:
            sb.__exit__(None, None, None)

    def detect(self) -> bool:
        return shutil.which("node") is not None
