import time
import random
from cache.redis_cache import set_cache

def ingest_realtime():
    while True:
        data = {
            "platform": random.choice(["TV", "YouTube", "Meta"]),
            "impressions": random.randint(5000, 50000),
            "clicks": random.randint(200, 3000),
            "conversions": random.randint(20, 400),
            "roi": round(random.uniform(1.0, 1.6), 2)
        }

        set_cache("latest_performance", data, ttl=300)
        print("Ingested:", data)
        time.sleep(10)

if __name__ == "__main__":
    ingest_realtime()
