import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tokensentinel.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                model_used TEXT,
                complexity_level TEXT,
                complexity_score REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                saved_tokens INTEGER,
                cost_total REAL,
                cost_saved REAL,
                latency_ms REAL,
                status TEXT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def log_request(data: dict):
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO requests 
               (request_id, model_used, complexity_level, complexity_score, 
                input_tokens, output_tokens, saved_tokens, cost_total, cost_saved, 
                latency_ms, status, error)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data.get("request_id", ""),
                data.get("model_used", ""),
                data.get("complexity_level", ""),
                data.get("complexity_score", 0),
                data.get("input_tokens", 0),
                data.get("output_tokens", 0),
                data.get("saved_tokens", 0),
                data.get("cost_total", 0),
                data.get("cost_saved", 0),
                data.get("latency_ms", 0),
                data.get("status", "success"),
                data.get("error", None),
            )
        )
        await db.commit()

async def get_metrics():
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        total_requests = await db.execute_fetchall("SELECT COUNT(*) as c FROM requests")
        total_tokens = await db.execute_fetchall("SELECT SUM(input_tokens + output_tokens) as c FROM requests")
        total_cost = await db.execute_fetchall("SELECT SUM(cost_total) as c FROM requests")
        total_saved = await db.execute_fetchall("SELECT SUM(cost_saved) as c FROM requests")
        avg_latency = await db.execute_fetchall("SELECT AVG(latency_ms) as c FROM requests")
        by_model = await db.execute_fetchall("SELECT model_used, COUNT(*) as count, SUM(cost_total) as cost FROM requests GROUP BY model_used ORDER BY count DESC LIMIT 5")
        by_complexity = await db.execute_fetchall("SELECT complexity_level, COUNT(*) as count FROM requests GROUP BY complexity_level")
        recent = await db.execute_fetchall("SELECT * FROM requests ORDER BY created_at DESC LIMIT 10")

    return {
        "total_requests": total_requests[0][0] if total_requests else 0,
        "total_tokens": total_tokens[0][0] if total_tokens else 0,
        "total_cost": round(total_cost[0][0], 6) if total_cost and total_cost[0][0] else 0,
        "total_saved": round(total_saved[0][0], 6) if total_saved and total_saved[0][0] else 0,
        "avg_latency_ms": round(avg_latency[0][0], 2) if avg_latency and avg_latency[0][0] else 0,
        "by_model": [{"model": r[0], "requests": r[1], "cost": r[2]} for r in by_model],
        "by_complexity": [{"level": r[0], "count": r[1]} for r in by_complexity],
        "recent_requests": [
            {"id": r[0], "model": r[2], "tokens": r[5]+r[6], "cost": r[8], "latency": r[9], "time": r[11]} 
            for r in recent
        ]
    }