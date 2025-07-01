from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    try:
        # Build the API URL
        url = f"https://api.exchangerate.host/convert?from={from_currency.upper()}&to={to_currency.upper()}&amount={amount}"

        # Call exchangerate.host API
        response = requests.get(url)
        data = response.json()

        # Check for valid result
        if response.status_code != 200 or "result" not in data or data["result"] is None:
            raise HTTPException(status_code=400, detail="Invalid API response or unsupported currency")

        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "converted_amount": data["result"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
