import subprocess
import sys

from backend.flask_setup import app


def init_tasks():
    for task in sys.argv[1:]:
        if task not in TASKS:
            raise SystemExit(f"Unknown task: {task}")
        TASKS[task]()


def _build():
    subprocess.run([sys.executable, "-m", "compileall", "."], check=True)


def _spotless_apply():
    """Add a noqa comment to ignore"""
    subprocess.run([sys.executable, "-m", "ruff", "format", "."], check=True)
    subprocess.run([sys.executable, "-m", "ruff", "check", "--fix", "."], check=True)


def _run_server():
    app.run(host="127.0.0.1", port=5000, debug=True)


TASKS = {
    "build": _build,
    "spotlessApply": _spotless_apply,
    "runServer": _run_server,
}
