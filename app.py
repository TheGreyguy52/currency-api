from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

API_KEY = "abc123"  # your secret key

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.headers.get("x-api-key") != API_KEY:
        return JSONResponse(status_code=403, content={"error": "Missing or invalid API key."})
    return await call_next(request)

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Currency conversion failed")
    data = response.json()
    return {"result": data["result"]}
