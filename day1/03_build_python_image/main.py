import redis
import socket
import logging
import os
import time
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from typing import Any

class CustomJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        json_string = json.dumps(content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":"))
        return (json_string + "\n").encode("utf-8")

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"default": {"format": "%(asctime)s [%(process)s] %(levelname)s: %(message)s"}},
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "INFO",
        },
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}

logging.config.dictConfig(LOG_CONFIG)

LOGGER = logging.getLogger("uvicorn.info")

level = os.environ.get("LOG_LEVEL", "INFO")
if level == "INFO":
    LOGGER.setLevel(logging.INFO)
if level == "DEBUG":
    LOGGER.setLevel(logging.DEBUG)


app = FastAPI()
hostname = socket.gethostname()
redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = os.environ.get("REDIS_PORT", 6379)
LOGGER.info(f"LOG_LEVEL has value {level}")
LOGGER.info(f"REDIS_HOST has value {redis_host}")
LOGGER.info(f"REDIS_PORT has value {redis_port}")

# Create a counter for tracking requests to /api/v1/info
info_requests_counter = Counter('info_requests_total', 'Total number of requests to /api/v1/info')

def get_redis():
    try:
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=0,
            socket_connect_timeout=3,  # Connection timeout in seconds
            socket_timeout=3  # Read/write timeout in seconds
        )
        r.ping()  # Test connection
        return r
    except (redis.ConnectionError, socket.gaierror) as e:
        LOGGER.error(f"Redis connection error: {e}")
        raise RuntimeError("Application cannot connect to Redis")

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/api/v1/info":
        info_requests_counter.inc()
    return response

@app.get("/", response_class=CustomJSONResponse)
async def root():
    return {"message": "Hello World", "hostname": hostname}

@app.get("/healthz", response_class=CustomJSONResponse)
async def healthz():
    try:
        r = get_redis()
        r.ping()
        return {"message": "Service is OK", "hostname": hostname}
    except (redis.ConnectionError, socket.gaierror) as e:
        LOGGER.error(f"Health check failed: {e}")
        return CustomJSONResponse(content={"message": "Service is NOT OK", "hostname": hostname}, status_code=500)
    except Exception as e:
        LOGGER.error(f"Unexpected error during health check: {e}")
        return CustomJSONResponse(content={"message": "Service is NOT OK", "hostname": hostname}, status_code=500)

@app.get("/api/v1/info", response_class=CustomJSONResponse)
async def info():
    try:
        started_at = time.time()
        r = get_redis()
        counter = r.get('counter')
        if counter is None:
            counter = 0
        else:
            counter = int(counter.decode('utf-8'))  # Decode and convert to integer
        LOGGER.info(f"counter var is {counter}")
        duration = time.time() - started_at
        LOGGER.debug(f"Request took {duration}")
        return {"message": "Counter", "hostname": hostname, "value": counter}
    except RuntimeError as e:
        LOGGER.error(f"Error in /api/v1/info: {e}")
        return CustomJSONResponse(content={"Can not connect to redis": str(e)}, status_code=500)

@app.post("/api/v1/info", response_class=CustomJSONResponse)
def info_post():
    try:
        started_at = time.time()
        r = get_redis()
        previous = r.get('counter')
        if previous is None:
            r.set('counter', 1)
        else:
            r.incr('counter')
        duration = time.time() - started_at
        LOGGER.debug(f"Request took {duration}")
        return {"message": "OK", "hostname": hostname}
    except RuntimeError as e:
        LOGGER.error(f"Error in /api/v1/info: {e}")
        return CustomJSONResponse(content={"Can not connect to redis": str(e)}, status_code=500)

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
