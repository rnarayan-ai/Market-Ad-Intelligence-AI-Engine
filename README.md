# Market-Ad-Intelligence-AI-Engine
An AI Agent for AIR (Audience, Inventory &amp; Reach) Data Analysis for advertising inventory &amp; performance. Goal is to Predict where, when, and on which platform an ad should air to maximize ROI, reach, and conversion.

# Market Intelligence Analysis — README

## Overview
This repository implements a lightweight market-intelligence pipeline that scans inventory, plans media buys, performs simple attribution and optimization, generates human-readable explanations using an LLM, and produces client reports (PPTX/PDF).

Key runtime entry points:
- API: [`app.main.recommend`](app/main.py) and [`app.main.generate_client_report`](app/main.py) — FastAPI app.
- Graph: [`graph.media_graph.build_graph`](graph/media_graph.py) — composes the processing graph.

## Architecture (high level)
- A state graph (see [`graph.media_graph.build_graph`](graph/media_graph.py)) sequences modular nodes:
  - Market scanning: [`agents.market_scanner.scan_market`](agents/market_scanner.py)
  - Planning: [`agents.planner_agent.plan_media`](agents/planner_agent.py)
  - Budget optimization (bandit): [`rl.rl_agent.BanditAgent`](rl/rl_agent.py) used in [`graph.media_graph.optimize_budget`](graph/media_graph.py)
  - Attribution: [`attribution.markov_attribution.markov_attribution`](attribution/markov_attribution.py)
  - Explanation (LLM + vector search): [`agents.explainer_agent.explain`](agents/explainer_agent.py)

The graph's typed state is defined as [`graph.state.MarketState`](graph/state.py).

## Components & Responsibilities
- Data ingestion
  - [`ingestion.realtime_ingest.ingest_realtime`](ingestion/realtime_ingest.py) — simple realtime loop that writes latest performance into Redis via [`cache.redis_cache.set_cache`](cache/redis_cache.py).
- Market scanner
  - [`agents.market_scanner.scan_market`](agents/market_scanner.py) — reads [data/inventory.csv](data/inventory.csv) and computes a score:
    $$
    score = \frac{\text{avg\_reach}}{\text{cost\_per\_slot}} \times (1 - \text{competition\_score})
    $$
  - Uses pandas and returns a ranked list placed into the graph state.
- Planner
  - [`agents.planner_agent.plan_media`](agents/planner_agent.py) — picks the top result from market scan into `media_plan`.
- Optimization (RL)
  - [`rl.rl_agent.BanditAgent`](rl/rl_agent.py) and [`rl.rl_environment.MediaEnvironment`](rl/rl_environment.py) — simple multi-armed bandit-style agent used by [`graph.media_graph.optimize_budget`](graph/media_graph.py).
  - Training script: [`rl.rl_trainer`](rl/rl_trainer.py).
- Attribution
  - [`attribution.markov_attribution.markov_attribution`](attribution/markov_attribution.py) — toy Markov-path counting attribution implementation.
- Vector search + explanations
  - [`vector_store.vector_db.build_vector_db`](vector_store/vector_db.py) and [`vector_store.vector_db.search_vector_db`](vector_store/vector_db.py) — uses HuggingFace embeddings + FAISS to store context snippets.
  - [`agents.explainer_agent.explain`](agents/explainer_agent.py) composes a prompt and calls the LLM via [`llm.groq_client.run_groq_query`](llm/groq_client.py).
- Reports
  - [`reports.report_generator.generate_reports`](reports/report_generator.py) — creates PPTX and PDF using:
    - [`reports.ppt_template.create_ppt`](reports/ppt_template.py)
    - [`reports.pdf_generator.create_pdf`](reports/pdf_generator.py)

## Key files (openable)
- Application & API
  - [app/main.py](app/main.py) — FastAPI app with endpoints [`app.main.recommend`](app/main.py) and [`app.main.generate_client_report`](app/main.py)
- Graph & State
  - [graph/media_graph.py](graph/media_graph.py) — [`graph.media_graph.build_graph`](graph/media_graph.py)
  - [graph/state.py](graph/state.py) — [`graph.state.MarketState`](graph/state.py)
- Agents
  - [agents/market_scanner.py](agents/market_scanner.py) — [`agents.market_scanner.scan_market`](agents/market_scanner.py)
  - [agents/planner_agent.py](agents/planner_agent.py) — [`agents.planner_agent.plan_media`](agents/planner_agent.py)
  - [agents/explainer_agent.py](agents/explainer_agent.py) — [`agents.explainer_agent.explain`](agents/explainer_agent.py)
- RL
  - [rl/rl_agent.py](rl/rl_agent.py) — [`rl.rl_agent.BanditAgent`](rl/rl_agent.py)
  - [rl/rl_environment.py](rl/rl_environment.py) — [`rl.rl_environment.MediaEnvironment`](rl/rl_environment.py)
  - [rl/rl_trainer.py](rl/rl_trainer.py)
- Vector store
  - [vector_store/vector_db.py](vector_store/vector_db.py) — [`vector_store.vector_db.build_vector_db`](vector_store/vector_db.py), [`vector_store.vector_db.search_vector_db`](vector_store/vector_db.py)
- Attribution
  - [attribution/markov_attribution.py](attribution/markov_attribution.py) — [`attribution.markov_attribution.markov_attribution`](attribution/markov_attribution.py)
- LLM
  - [llm/groq_client.py](llm/groq_client.py) — [`llm.groq_client.run_groq_query`](llm/groq_client.py)
  - [llm/llm_config.py](llm/llm_config.py) — local ChatOpenAI wrapper (unused in current explain agent)
- Cache
  - [cache/redis_cache.py](cache/redis_cache.py) — [`cache.redis_cache.redis_client`](cache/redis_cache.py), [`cache.redis_cache.get_cache`](cache/redis_cache.py), [`cache.redis_cache.set_cache`](cache/redis_cache.py)
- Reports & templates
  - [reports/report_generator.py](reports/report_generator.py)
  - [reports/ppt_template.py](reports/ppt_template.py)
  - [reports/pdf_generator.py](reports/pdf_generator.py)
- Data
  - [data/inventory.csv](data/inventory.csv)
  - [data/campaigns.csv](data/campaigns.csv)
  - [data/audience.csv](data/audience.csv)
- Misc
  - [ingestion/realtime_ingest.py](ingestion/realtime_ingest.py)
  - [vector_store/vector_db.py](vector_store/vector_db.py)
  - [requirements.txt](requirements.txt)

## Setup & Run
1. Create virtualenv and install:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
