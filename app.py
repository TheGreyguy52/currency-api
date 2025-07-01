from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Currency conversion failed")
    
    data = response.json()
    return {"result": data["result"]}
