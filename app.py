from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

API_KEY = "YOUR_API_KEY_HERE"  # ⬅️ PUT YOUR apilayer API key here
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"

@app.get("/convert")
def convert_currency(
    from_currency: str = Query(..., alias="from_currency"),
    to_currency: str = Query(..., alias="to_currency"),
    amount: float = Query(...)
):
    headers = {
        "apikey": API_KEY
    }

    params = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        data = response.json()

        if response.status_code != 200 or "result" not in data:
            raise HTTPException(status_code=response.status_code, detail=data.get("error", "Conversion failed"))

        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "converted_amount": data["result"]
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
