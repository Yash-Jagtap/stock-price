from fastapi import FastAPI, WebSocket
import requests
from dotenv import load_dotenv
import os
import json
# Load variables from .env file
load_dotenv()

app = FastAPI()

# Fetch stock data from a public API
API_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv('alpha_vantage_key')

@app.get("/stock/{symbol}")
async def get_stock_price(symbol: str):
    """Fetch stock price for a given symbol."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY,
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    try:
        # Extract the latest price
        latest_data = list(data["Time Series (1min)"].values())[0]
        return {"symbol": symbol, "price": latest_data["1. open"]}
    except KeyError:
        return {"error": "Invalid symbol or API limit reached"}
@app.get("/")
async def homepage():
    return {"response":"Hola!"}
@app.websocket("/ws/{symbol}")
async def stock_price_websocket(websocket: WebSocket, symbol: str):
    """Real-time updates using WebSocket."""
    await websocket.accept()
    while True:
        stock_data = await get_stock_price(symbol)
        await websocket.send_json(stock_data)

@app.get("/getall/{symbol}")
async def get_all_history(symbol):
    with open("stock_price.json",'r') as f:
        data = f.read()
        data = json.loads(data)
    return data[symbol]
