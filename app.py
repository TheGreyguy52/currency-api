from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch from currency API")

    data = response.json()

    if not data.get("success"):
        raise HTTPException(status_code=400, detail="Invalid or unsupported currency conversion.")

    result = data.get("result")
    if result is None:
        raise HTTPException(status_code=400, detail="No result returned.")

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": result
    }
