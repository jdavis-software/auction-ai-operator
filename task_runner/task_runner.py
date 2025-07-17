"""task_runner.py

Scans the /tasks/ directory for .task.json files and executes corresponding
agent scripts. Logs output to /logs/ and archives processed tasks.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT_DIR / "tasks"
LOGS_DIR = ROOT_DIR / "logs"
ARCHIVE_DIR = TASKS_DIR / "archive"

# ---------------------------------------------------------------------------
# Agent mapping
# ---------------------------------------------------------------------------
AGENT_MAP: Dict[str, Path] = {
    "gsa_scraper": ROOT_DIR / "agents" / "scraper" / "gsa" / "gsa_scraper.py",
    "nyc_scraper": ROOT_DIR / "agents" / "scraper" / "nyc" / "nyc_scraper.py",
    "normalize_data": ROOT_DIR / "agents" / "normalizer" / "normalize.py",
    "check_compliance": ROOT_DIR / "agents" / "compliance" / "check.py",
    "generate_outreach": ROOT_DIR / "agents" / "outreach" / "contact_copart.py",
    "push_repo": ROOT_DIR / "agents" / "push_repo" / "commit_push.py",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ensure_directories() -> None:
    """Create required directories if they don't exist."""
    for d in (TASKS_DIR, LOGS_DIR, ARCHIVE_DIR):
        d.mkdir(parents=True, exist_ok=True)


def run_agent(script_path: Path, params: Dict[str, Any] | None = None) -> tuple[str, str]:
    """Run the agent script via subprocess and return (stdout, stderr)."""
    cmd = [sys.executable, str(script_path)]
    if params:
        # Pass params as a JSON string argument
        cmd.append(json.dumps(params))

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate()
    return stdout, stderr


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def process_tasks() -> None:
    ensure_directories()

    for task_file in TASKS_DIR.glob("*.task.json"):
        try:
            task_json = json.loads(task_file.read_text())
            agent_key: str | None = task_json.get("agent")
            params: Dict[str, Any] | None = task_json.get("params")

            if not agent_key:
                print(f"[WARN] Missing 'agent' in {task_file.name}; skipping.")
                continue

            script_path = AGENT_MAP.get(agent_key)
            if not script_path or not script_path.exists():
                print(f"[WARN] Unknown or missing agent script for key '{agent_key}'.")
                continue

            print(f"[INFO] Running agent '{agent_key}' for task {task_file.name} ...")
            stdout, stderr = run_agent(script_path, params)

            # Write log
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            log_file = LOGS_DIR / f"{agent_key}_{timestamp}.log"
            with log_file.open("w", encoding="utf-8") as lf:
                lf.write(f"# Command: python {script_path}\n")
                if params:
                    lf.write(f"# Params: {json.dumps(params)}\n")
                lf.write("\n=== STDOUT ===\n")
                lf.write(stdout)
                lf.write("\n=== STDERR ===\n")
                lf.write(stderr)

            # Archive task file
            shutil.move(str(task_file), ARCHIVE_DIR / task_file.name)
            print(f"[DONE] Task {task_file.name} processed. Log: {log_file.name}")

        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] Failed processing {task_file.name}: {exc}")


if __name__ == "__main__":
    process_tasks()
