from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert"
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Currency conversion failed")

    data = response.json()

    if data.get("result") is None:
        raise HTTPException(status_code=500, detail="Invalid API response or unsupported currency")

    return {"result": data["result"]}
