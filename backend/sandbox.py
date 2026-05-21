import tempfile
import subprocess
import shutil
import time

class Sandbox:
    def __init__(self, timeout=30, max_output=1048576):
        self.timeout = timeout
        self.max_output = max_output

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="dsa_")
        return self

    def __exit__(self, *args):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run(self, cmd, cwd, input_data=None):
        start = time.time()
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
        )
        try:
            stdout, stderr = proc.communicate(input=input_data, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            return {
                "stdout": stdout[:self.max_output],
                "stderr": stderr[:self.max_output] + f"\n[TIMEOUT: Process killed after {self.timeout}s]",
                "exit_code": -1,
                "timing_ms": int((time.time() - start) * 1000),
            }
        elapsed = int((time.time() - start) * 1000)
        return {
            "stdout": stdout[:self.max_output],
            "stderr": stderr[:self.max_output],
            "exit_code": proc.returncode,
            "timing_ms": elapsed,
        }
