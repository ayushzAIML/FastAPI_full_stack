from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.schema import CarFeatures , PredictionResponse
from app.model import predict_price , load_artifacts
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Car Price Prediction API" ,
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_methods = ["*"]
)

@app.on_event("startup")

def startup_event():
    load_artifacts()

@app.get("/test")
def test():
    return JSONResponse(status_code=200,
                        content={"Success":True,
                        "message":"this is test route"})


@app.post("/predict",response_model=PredictionResponse)
def health(features: CarFeatures):
    price = predict_price(features.model_dump())
    return PredictionResponse(prediction_price=price)

