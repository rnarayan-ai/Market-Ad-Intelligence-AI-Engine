from langgraph.graph import StateGraph
from agents.explainer_agent import explain
from agents.market_scanner import scan_market
from agents.planner_agent import MarketState, plan_media
from vector_store import vector_db
from rl.rl_agent import BanditAgent
from cache.redis_cache import get_cache
from attribution.markov_attribution import markov_attribution


def optimize_budget(state: MarketState)-> MarketState:
    agent = BanditAgent(3)
    state["budget_strategy"] = {"budget_strategy": agent.q_values.tolist()}
    return state

def attribution_step(state: MarketState) -> MarketState:
    paths = state.get("paths", [])
    state["attribution"] = {"attribution": markov_attribution(paths)}
    return state
    
def build_graph():
  
    graph = StateGraph(MarketState)

    graph.add_node("scan", scan_market)
    graph.add_node("plan", plan_media)
    graph.add_node("optimize_budget", optimize_budget)
    graph.add_node("attribution", attribution_step)
    graph.add_node("explain", explain)

    graph.set_entry_point("scan")
    graph.add_edge("scan", "plan")
    graph.add_edge("plan", "optimize_budget")
    graph.add_edge("optimize_budget", "attribution")
    graph.add_edge("attribution", "explain")

    return graph.compile()
