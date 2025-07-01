from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import logging

# Initialize app
app = FastAPI(title="Currency Converter API", version="1.0")

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Supported currencies (you can expand this list or fetch dynamically)
SUPPORTED_CURRENCIES = {"USD", "EUR", "PHP", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SGD"}

@app.get("/convert", summary="Convert currency", description="Converts amount from one currency to another.")
def convert_currency(
    from_currency: str = Query(..., description="Currency to convert from, e.g., USD"),
    to_currency: str = Query(..., description="Currency to convert to, e.g., EUR"),
    amount: float = Query(..., gt=0, description="Amount to convert (must be greater than 0)")
):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    # ✅ Validate currency input
    if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
        raise HTTPException(
            status_code=400,
            detail=f"One or both currencies are not supported. Supported: {', '.join(sorted(SUPPORTED_CURRENCIES))}"
        )

    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200 or "result" not in data or data["result"] is None:
            raise HTTPException(status_code=502, detail="Failed to get valid response from currency service.")

        converted = round(data["result"], 2)

        return JSONResponse(content={
            "from": from_currency,
            "to": to_currency,
            "original_amount": amount,
            "converted_amount": converted,
            "rate_used": data.get("info", {}).get("rate"),
            "provider": "exchangerate.host"
        })

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise HTTPException(status_code=503, detail="External API is unavailable.")
