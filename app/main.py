from fastapi import FastAPI
from graph.media_graph import build_graph
from reports.report_generator import generate_reports
from cache.redis_cache import redis_client

app = FastAPI()
graph = build_graph()

@app.on_event("startup")
async def startup_event():
    print("🚀 Market Intelligent Analysis backend starting...")
    # test redis connection
    try:
        redis_client.ping()
        print("✅ Redis connected")
        
    except Exception as e:
        print("❌ Redis not connected:", e)
        

@app.get("/recommend")
def recommend():
    final_state = graph.invoke({})
    explanation = final_state.get("explanation", "No explanation generated")
    print(f"RESULT Post Graph Completion : {explanation}")
    #print("FINAL STATE KEYS:", list(final_state.keys()))
    #print("FINAL STATE CONTENT:", final_state)
    return final_state

@app.get("/generate-report")
def generate_client_report():
    decision = graph.invoke({})

    report_data = {
        "client": "Client A",
        "platform": decision["platform"],
        "time_band": decision["time_band"],
        "region": "Tier-2",
        "expected_roi": "1.42x",
        "confidence": "High",
        "explanation": decision.get("explanation", "AI generated insight")
    }

    files = generate_reports(report_data)
    return files