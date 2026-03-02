# FastAPI Integration Example

This example shows a production-oriented integration pattern.

## 1) Add middleware-style tracking

```python
from fastapi import FastAPI, Request
from transparency import TransparencyLayer

app = FastAPI()
transparency = TransparencyLayer(agent_name="fastapi-agent", storage_path="./sessions")

@app.middleware("http")
async def track_requests(request: Request, call_next):
    transparency.track_action(
        action_type="request",
        input_data={"path": request.url.path, "method": request.method},
        output_data="processing",
    )
    response = await call_next(request)
    transparency.track_action(
        action_type="response",
        input_data={"path": request.url.path},
        output_data={"status_code": response.status_code},
    )
    return response
```

## 2) Add auth + rate limiting

Use your existing auth stack (JWT/session) and apply a limiter (e.g. SlowAPI) before invoking agent logic.

## 3) Persist transparency records

Store generated JSON sessions in object storage (S3/GCS) or a mounted volume for retention and compliance.

## 4) Operational checklist

- redact sensitive payload fields before `track_action`
- rotate old session files with retention rules
- alert on suspicious action patterns (high tool error rates, repeated retries)
