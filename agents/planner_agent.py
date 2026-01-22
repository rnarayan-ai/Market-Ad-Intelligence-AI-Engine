from typing import TypedDict, List

from graph.state import MarketState

def plan_media(state: MarketState) -> MarketState:
    if "market_scan" not in state:
        raise RuntimeError(
            f"'market_scan' missing. Available keys: {list(state.keys())}"
            f"STATE KEYS: {list(state.keys())}"
        )
    market_data = state["market_scan"]
    #print(f"market_data in Planner Node : {market_data}")
    top = market_data[0]
    state["media_plan"] = {
        "platform": top["platform"],
        "time_band": top["time_band"],
        "confidence": "High"
    }
    #print(f"STATE KEYS in Planner Node : {list(state.keys())}")
    return state
