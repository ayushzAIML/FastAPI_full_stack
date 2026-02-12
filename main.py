from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import CarFeatures , PredictionResponse
from model import predict_price , load_artifacts
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Car Price Prediction API" ,
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.on_event("startup")

def startup_event():
    load_artifacts()
 
@app.get("/")
def root():
    return JSONResponse(status_code=200,
                        content={"Success":True,
                        "message":"Car Price Prediction API is running"})




@app.post("/predict",response_model=PredictionResponse)
def health(features: CarFeatures):
    price = predict_price(features.model_dump())
    return PredictionResponse(prediction_price=price)

