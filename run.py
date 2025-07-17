"""
Entry point for the auction‑ai‑operator project.
"""
from auction_ai_operator.orchestrator import Orchestrator


if __name__ == "__main__":
    Orchestrator().run()
