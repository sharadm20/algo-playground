import shutil
from .base import BaseRunner
from sandbox import Sandbox
from models import RunResponse

class JavaRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as sb:
            class_name = "Main"
            filepath = f"{sb.temp_dir}/{class_name}.java"
            with open(filepath, "w") as f:
                f.write(code)
            build = sb.run(["javac", filepath], sb.temp_dir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = sb.run(["java", "-cp", sb.temp_dir, class_name], sb.temp_dir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("javac") is not None


class CRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as sb:
            filepath = f"{sb.temp_dir}/program.c"
            binary = f"{sb.temp_dir}/program"
            with open(filepath, "w") as f:
                f.write(code)
            build = sb.run(["gcc", filepath, "-o", binary], sb.temp_dir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = sb.run([binary], sb.temp_dir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("gcc") is not None


class GoRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as sb:
            filepath = f"{sb.temp_dir}/main.go"
            with open(filepath, "w") as f:
                f.write(code)
            result = sb.run(["go", "run", filepath], sb.temp_dir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("go") is not None
