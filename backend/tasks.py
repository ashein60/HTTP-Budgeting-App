import subprocess
import sys

from backend.database_setup import init_all_seed_data
from backend.flask_handler import app


def init_tasks():
    for task in sys.argv[1:]:
        if task not in TASKS:
            raise SystemExit(f"Unknown task: {task}")
        TASKS[task]()


def _build():
    subprocess.run([sys.executable, "-m", "compileall", "."], check=True)


def _create_seed_data():
    init_all_seed_data()


def _spotless_apply():
    """Add # noqa # isort: skip comments to ignore"""
    subprocess.run([sys.executable, "-m", "ruff", "format", "."], check=True)
    subprocess.run([sys.executable, "-m", "ruff", "check", "--fix", "."], check=True)


def _start_server():
    app.run(host="127.0.0.1", port=5000, debug=True)


TASKS = {
    "build": _build,
    "createSeedData": _create_seed_data,
    "spotlessApply": _spotless_apply,
    "startServer": _start_server,
}
