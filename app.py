from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    try:
        response = requests.get(
            "https://api.exchangerate.host/convert",
            params={
                "from": from_currency,
                "to": to_currency,
                "amount": amount
            }
        )
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {e}")

    if not data.get("success"):
        raise HTTPException(status_code=400, detail="Invalid or unsupported currency conversion.")

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": data["result"]
    }
