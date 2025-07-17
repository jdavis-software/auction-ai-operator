import asyncio
from typing import Any, Dict

from .scheduler import build_scheduler
from .agents.scraper import ScraperAgent
from .agents.compliance import ComplianceAgent
from .agents.normalization import NormalizationAgent
from .agents.outreach import OutreachAgent


class Orchestrator:
    """Coordinates all agents through an async event loop."""

    def __init__(self) -> None:
        self.scraper = ScraperAgent()
        self.compliance = ComplianceAgent()
        self.normalizer = NormalizationAgent()
        self.outreach = OutreachAgent()

        # Build a scheduler for time‑based triggers
        self.scheduler = build_scheduler()
        self.event_queue: asyncio.Queue[str] = asyncio.Queue()

    # --------------------------------------------------------------------- #
    # Scheduling / event helpers
    # --------------------------------------------------------------------- #
    def _schedule_jobs(self) -> None:
        """Add cron / interval jobs here. E.g., scrape every 5 minutes."""
        self.scheduler.add_job(
            lambda: asyncio.create_task(self.event_queue.put("scrape")),
            "interval",
            minutes=5,
            id="scrape_job",
        )

    # --------------------------------------------------------------------- #
    # Event loop
    # --------------------------------------------------------------------- #
    async def _event_loop(self) -> None:
        """Central loop: waits for events, then runs agents in order."""
        self._schedule_jobs()

        while True:
            event = await self.event_queue.get()

            try:
                if event == "scrape":
                    data = await self.scraper.run()

                    # Compliance check
                    compliant_data = await self.compliance.run(data)

                    # Normalize
                    normalized_data = await self.normalizer.run(compliant_data)

                    # Outreach
                    await self.outreach.run(normalized_data)

            except Exception as exc:  # noqa: BLE001
                # TODO: add robust logging / alerting
                print(f"[ERROR] {exc}")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def run(self) -> None:
        """Starts the orchestrator. Blocks until interrupted."""
        try:
            asyncio.run(self._event_loop())
        except KeyboardInterrupt:
            print("Shutting down orchestrator...")
