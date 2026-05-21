from .python_runner import PythonRunner
from .rust_runner import RustRunner
from .js_runner import JsRunner
from .other_runners import JavaRunner, CRunner, GoRunner

RUNNERS = {
    "python": PythonRunner,
    "rust": RustRunner,
    "javascript": JsRunner,
    "java": JavaRunner,
    "c": CRunner,
    "go": GoRunner,
}
