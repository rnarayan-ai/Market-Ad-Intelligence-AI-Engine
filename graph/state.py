from typing import TypedDict, List, Dict

class MarketState(TypedDict, total=False):
    market_scan: List[Dict]
    media_plan: Dict
    explanation: str
