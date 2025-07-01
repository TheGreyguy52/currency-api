from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="Ultimate Currency Converter API",
    description="Converts currency using exchangerate.host. Supports all ISO currency codes.",
    version="2.0"
)

@app.get("/convert", summary="Currency Conversion Endpoint")
def convert_currency(
    from_currency: str = Query(..., description="Currency code to convert from (e.g., USD)"),
    to_currency: str = Query(..., description="Currency code to convert to (e.g., EUR)"),
    amount: float = Query(..., gt=0, description="Amount to convert (must be greater than 0)")
):
    try:
        # Normalize input
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        # Validate currency format
        if not from_currency.isalpha() or not to_currency.isalpha():
            raise HTTPException(status_code=400, detail="Currency codes must be valid alphabetic values like 'USD' or 'EUR'.")

        # Build API URL
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        headers = {"User-Agent": "Mozilla/5.0"}

        # Request conversion data
        response = requests.get(url, headers=headers, timeout=10)

        # Check HTTP status
        if response.status_code != 200:
            logging.error(f"Currency API status error: {response.status_code}")
            raise HTTPException(status_code=502, detail="Currency provider service is currently unreachable or failed to respond.")

        data = response.json()

        # Validate response structure
        if not data.get("success"):
            logging.warning(f"API returned unsuccessful: {data}")
            raise HTTPException(status_code=400, detail="Invalid or unsupported currency conversion.")

        if "result" not in data or data["result"] is None:
            logging.warning(f"No result in response: {data}")
            raise HTTPException(status_code=400, detail="Conversion result is missing or invalid.")

        converted_amount = round(data["result"], 2)
        rate_used = data.get("info", {}).get("rate", "N/A")

        # Final structured response
        return JSONResponse(content={
            "status": "success",
            "from": from_currency,
            "to": to_currency,
            "original_amount": amount,
            "converted_amount": converted_amount,
            "rate_used": rate_used,
            "provider": "exchangerate.host"
        })

    # Handle timeouts
    except requests.exceptions.Timeout:
        logging.exception("Timeout while contacting API.")
        raise HTTPException(status_code=504, detail="Currency provider timed out. Please try again later.")

    # Handle connection errors
    except requests.exceptions.ConnectionError:
        logging.exception("Connection error to currency provider.")
        raise HTTPException(status_code=503, detail="Failed to connect to the currency provider.")

    # Handle any unknown errors
    except Exception as e:
        logging.exception("Unexpected error:")
        raise HTTPException(status_code=500, detail=f"Unexpected internal error: {str(e)}")
