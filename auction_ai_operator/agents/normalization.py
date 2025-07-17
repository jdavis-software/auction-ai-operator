import asyncio
from typing import List, Dict, Any


class NormalizationAgent:
    """Cleans and structures raw data into a consistent schema."""

    async def run(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print("[NormalizationAgent] Normalizing data...")
        await asyncio.sleep(0.5)  # simulate processing
        normalized = []
        for item in items:
            normalized.append(
                {
                    "id": item["id"],
                    "title": item["title"].strip(),
                    "price_usd": float(item["price"].replace("$", "")),
                }
            )
        print("[NormalizationAgent] Normalization complete.")
        return normalized
