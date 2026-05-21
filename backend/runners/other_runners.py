import shutil
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import RunResponse

class JavaRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        sb = Sandbox()
        tmpdir = sb.__enter__()
        try:
            class_name = "Main"
            filepath = f"{tmpdir}/{class_name}.java"
            with open(filepath, "w") as f:
                f.write(code)
            build = sb.run(["javac", filepath], tmpdir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = sb.run(["java", "-cp", tmpdir, class_name], tmpdir)
            return self._make_response(result)
        finally:
            sb.__exit__(None, None, None)

    def detect(self) -> bool:
        return shutil.which("javac") is not None


class CRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        sb = Sandbox()
        tmpdir = sb.__enter__()
        try:
            filepath = f"{tmpdir}/program.c"
            binary = f"{tmpdir}/program"
            with open(filepath, "w") as f:
                f.write(code)
            build = sb.run(["gcc", filepath, "-o", binary], tmpdir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = sb.run([binary], tmpdir)
            return self._make_response(result)
        finally:
            sb.__exit__(None, None, None)

    def detect(self) -> bool:
        return shutil.which("gcc") is not None


class GoRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        sb = Sandbox()
        tmpdir = sb.__enter__()
        try:
            filepath = f"{tmpdir}/main.go"
            with open(filepath, "w") as f:
                f.write(code)
            result = sb.run(["go", "run", filepath], tmpdir)
            return self._make_response(result)
        finally:
            sb.__exit__(None, None, None)

    def detect(self) -> bool:
        return shutil.which("go") is not None
