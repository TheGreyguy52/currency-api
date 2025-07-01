from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

ACCESS_KEY = "837066195c3e07fb2f8d4e180b95de3"

@app.get("/convert")
def convert(
    from_: str = Query(..., alias="from"),
    to: str = Query(...),
    amount: float = Query(...)
):
    url = (
        f"https://api.exchangerate.host/convert"
        f"?from={from_}&to={to}&amount={amount}&access_key={ACCESS_KEY}"
    )
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Currency service failed: {str(e)}")

    if not data.get("success"):
        error_info = data.get("error", {}).get("info", "Unknown error")
        raise HTTPException(status_code=400, detail=f"Conversion failed: {error_info}")

    result = data.get("result")
    if result is None:
        raise HTTPException(status_code=400, detail="No conversion result returned")

    return {
        "from": from_,
        "to": to,
        "amount": amount,
        "converted": result
    }
