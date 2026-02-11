from pydantic import BaseModel , Field
from enum import Enum



class FuelType(str,Enum):
    petrol = "Petrol"
    diesel = "Diesel"
    cng = "CNG"

class SellerType(str , Enum):
    dealer = "Dealer"
    individual = "Individual"

class TransmissionType(str , Enum):
    manual = "Manual"
    automatic = "Automatic"

class CarFeatures(BaseModel):
    Car_Name : str = Field(...,examples=["ritz"])
    year : int = Field(...,examples=[2014])
    Present_price : float = Field(...,examples=[5.59])
    Kms_Driven : int = Field(...,examples=[27000])
    Fuel_Type :FuelType
    Seller_Type:SellerType
    Transmission:TransmissionType
    owner: int = Field(...,ge=0,le=3,examples=[0], description= "Numbers of previous owners (0,1 or 3)")

class PredictionResponse(BaseModel):
    prediction_price : float