from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src import inference
from src import gemini_narration


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(inference.preload_all)
    yield


app = FastAPI(title="RaksaDana API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuantityDetail(BaseModel):
    shares: int
    lots: float
    lot_size: int


class PredictionResponse(BaseModel):
    ticker: str
    signal_date: str
    base_close: float
    predicted_log_return: float
    predicted_close: float
    signal: Literal["BUY", "HOLD", "SELL"]
    narration: str | None = None


class ForecastPoint(BaseModel):
    date: str
    predicted_close: float
    predicted_log_return: float


class MetricsResponse(BaseModel):
    ticker: str
    mape: float
    r2: float
    direction_accuracy: float
    return_rmse: float


class ProfitLossRequest(BaseModel):
    ticker: str
    buy_price: float
    lots: int | None = None
    shares: int | None = None
    sell_price: float | None = None
    forecast_days: int | None = None
    buy_fee_rate: float = 0.0015
    sell_fee_rate: float = 0.0025
    lot_size: int = 100


class ProfitLossResponse(BaseModel):
    ticker: str
    status: Literal["PROFIT", "LOSS", "BREAK_EVEN"]
    price_source: str
    exit_date: str | None
    quantity: QuantityDetail
    buy_price: float
    sell_price: float
    gross_buy_value: float
    buy_fee: float
    total_cost: float
    gross_sell_value: float
    sell_fee: float
    net_proceeds: float
    gross_profit_loss: float
    net_profit_loss: float
    net_return_pct: float
    price_change_pct: float
    breakeven_sell_price: float
    assumptions: dict
    narration: str | None = None


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "tickers": inference.SUPPORTED_TICKERS}


@app.get("/api/v1/tickers")
def tickers():
    return inference.SUPPORTED_TICKERS


@app.get("/api/v1/predict/{ticker}", response_model=PredictionResponse)
async def predict(ticker: str, narrate: bool = Query(False)):
    try:
        result = await asyncio.to_thread(inference.predict_next_day, ticker)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if narrate:
        try:
            metrics_data = await asyncio.to_thread(inference.get_metrics, ticker)
            result["narration"] = await asyncio.to_thread(
                gemini_narration.generate_prediction_narration,
                ticker,
                result.copy(),
                metrics_data,
            )
        except Exception as e:
            result["narration"] = f"Narasi tidak tersedia: {e}"

    return result


@app.get("/api/v1/metrics/{ticker}", response_model=MetricsResponse)
async def metrics(ticker: str):
    result = await asyncio.to_thread(inference.get_metrics, ticker)
    if not result:
        raise HTTPException(status_code=404, detail=f"No metrics found for {ticker}")
    return result


@app.get("/api/v1/forecast/{ticker}", response_model=list[ForecastPoint])
async def forecast(ticker: str, days: int = Query(30, ge=1, le=90)):
    try:
        return await asyncio.to_thread(inference.forecast_30d, ticker, days)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/api/v1/profit-loss", response_model=ProfitLossResponse)
async def profit_loss(body: ProfitLossRequest, narrate: bool = Query(False)):
    try:
        result = await asyncio.to_thread(
            inference.calculate_profit_loss,
            ticker=body.ticker,
            buy_price=body.buy_price,
            lots=body.lots,
            shares=body.shares,
            sell_price=body.sell_price,
            forecast_days=body.forecast_days,
            buy_fee_rate=body.buy_fee_rate,
            sell_fee_rate=body.sell_fee_rate,
            lot_size=body.lot_size,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if narrate:
        try:
            prediction = await asyncio.to_thread(inference.predict_next_day, body.ticker)
            metrics_data = await asyncio.to_thread(inference.get_metrics, body.ticker)
            result["narration"] = await asyncio.to_thread(
                gemini_narration.generate_profit_loss_narration,
                body.ticker,
                prediction,
                metrics_data,
                result.copy(),
            )
        except Exception as e:
            result["narration"] = f"Narasi tidak tersedia: {e}"

    return result


if os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse("frontend/dist/index.html")
