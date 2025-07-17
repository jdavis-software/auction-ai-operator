import asyncio
from typing import List, Dict, Any


class ScraperAgent:
    """Collects auction data from external sources."""

    async def run(self) -> List[Dict[str, Any]]:
        print("[ScraperAgent] Starting scrape...")
        await asyncio.sleep(1)  # simulate I/O
        data = [
            {"id": 1, "title": "Antique Vase", "price": "$100"},
            {"id": 2, "title": "Vintage Watch", "price": "$250"},
        ]
        print("[ScraperAgent] Scrape finished.")
        return data
