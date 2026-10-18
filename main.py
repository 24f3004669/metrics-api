import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "24f3004669@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-2xgg0l.example.com"

app = FastAPI()

# 1) CORS: only the assigned origin is allowed (no "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


# 2) Add X-Request-ID and X-Process-Time to EVERY response.
# This is added after CORS, so it wraps it and also covers preflights.
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/stats")
def stats(values: str = ""):
    try:
        nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")
    if not nums:
        raise HTTPException(status_code=400, detail="no values provided")

    total = sum(nums)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }