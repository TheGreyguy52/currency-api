from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Exchange API failed with status {response.status_code}")

    data = response.json()
    if not data.get("success"):
        raise HTTPException(status_code=400, detail="Invalid or unsupported currency conversion.")

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": data["result"]
    }
