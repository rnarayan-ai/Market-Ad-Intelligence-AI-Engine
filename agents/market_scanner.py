import pandas as pd
#from cache.redis_cache import get_cache, set_cache
from typing import TypedDict, List

from graph.state import MarketState


def scan_market(state: MarketState) -> MarketState:
    #cached = None #get_cache("market_scan")
    #if cached:
     #   state["market_scan"] = cached
      #  return state

    inventory = pd.read_csv("data/inventory.csv")
    inventory["score"] = (
        inventory["avg_reach"] / inventory["cost_per_slot"]
    ) * (1 - inventory["competition_score"])

    result = inventory.sort_values("score", ascending=False).to_dict("records")
    #set_cache("market_scan", result)
    state["market_scan"] = result
    #print(f"STATE KEYS: {list(state.keys())}")
    return state
