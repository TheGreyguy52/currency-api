from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import logging
from typing import Optional

# App metadata
app = FastAPI(
    title="Ultimate Currency Converter API",
    description="Reliable and safe currency conversion using exchangerate.host API",
    version="2.0"
)

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.get("/convert", summary="Currency Converter")
def convert_currency(
    from_currency: str = Query(..., description="Currency code to convert from (e.g., USD)"),
    to_currency: str = Query(..., description="Currency code to convert to (e.g., EUR)"),
    amount: float = Query(..., gt=0, description="Amount to convert (must be a number greater than 0)")
):
    try:
        # Clean and validate input
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        if not from_currency.isalpha() or not to_currency.isalpha():
            raise HTTPException(status_code=400, detail="Currency codes must contain only letters (e.g., USD, EUR)")

        # Build URL
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        logging.info(f"Requesting conversion: {url}")

        # Make the API request
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logging.error(f"External API error: {response.status_code}")
            raise HTTPException(status_code=502, detail="Currency provider failed to respond correctly.")

        data = response.json()

        # Validate response structure
        if not data.get("success") or "result" not in data or data["result"] is None:
            logging.warning(f"Bad API response: {data}")
            raise HTTPException(status_code=400, detail="Invalid currency pair or response data.")

        # Extract result
        converted = round(data["result"], 2)
        rate_used = data.get("info", {}).get("rate", "N/A")

        result = {
            "status": "success",
            "from": from_currency,
            "to": to_currency,
            "original_amount": amount,
            "converted_amount": converted,
            "rate_used": rate_used,
            "provider": "exchangerate.host"
        }

        return JSONResponse(content=result, status_code=200)

    except requests.exceptions.Timeout:
        logging.exception("Timeout connecting to exchange API.")
        raise HTTPException(status_code=504, detail="Currency API timeout. Try again later.")
    
    except requests.exceptions.ConnectionError:
        logging.exception("Connection error to exchange API.")
        raise HTTPException(status_code=503, detail="Currency API unreachable. Please check your network.")
    
    except Exception as e:
        logging.exception("Unexpected error during currency conversion.")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
