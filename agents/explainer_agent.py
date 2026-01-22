#from llm.llm_config import llm
from llm.groq_client import run_groq_query
from vector_store.vector_db import search_vector_db
from typing import Dict, TypedDict, List
from vector_store import vector_db

from graph.state import MarketState
    
texts = [
        "YouTube evening slots perform well in Tier-2 cities",
        "Lower competition increases ROI",
        "Meta works better for remarketing"
    ]
# Build vector DB once globally
vector_db_global = vector_db.build_vector_db(texts)

def explain(state: MarketState) -> MarketState:
        if "media_plan" not in state:
            raise RuntimeError(
                f"'media_plan' missing. Available keys: {list(state.keys())}"
            )

        decision = state["media_plan"]
        #print(f"media_plan decision in Explain Node : {decision}")
        
        context_docs = search_vector_db(
            vector_db_global,
            f"{decision['platform']} {decision['time_band']} performance"
        )

        context = " ".join([d.page_content for d in context_docs])

        prompt = f"""
        Explain to a media agency client why this plan is recommended.
        Decision: {decision}
        Context: {context}
        """

        final_response = run_groq_query(prompt)
        #print(f"final_response in Explain Node : {final_response}")
        state["explanation"] = final_response
        #print(f"STATE KEYS in Explan Node : {list(state.keys())}")
        return state
