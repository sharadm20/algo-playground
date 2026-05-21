import shutil
import os
from ..models import RunResponse
from .base import BaseRunner

class RustRunner(BaseRunner):
    TEMPLATE = """fn main() {{
    {}
}}"""

    def execute(self, code: str) -> RunResponse:
        wrapped = self.TEMPLATE.format(code) if "fn main" not in code else code
        with self.sandbox as sb:
            src_dir = f"{sb.temp_dir}/src"
            os.makedirs(src_dir, exist_ok=True)
            with open(f"{src_dir}/main.rs", "w") as f:
                f.write(wrapped)
            with open(f"{sb.temp_dir}/Cargo.toml", "w") as f:
                f.write('[package]\nname = "temp"\nversion = "0.1.0"\nedition = "2021"\n')
            result = sb.run(["cargo", "run", "-q"], sb.temp_dir)
            tests = BaseRunner.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("cargo") is not None

