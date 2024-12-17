from fastapi import APIRouter, Depends, HTTPException, status
from services.fund_service import get_open_schmes 
from auth.jwt import get_user_id
from pydantic import BaseModel
from typing import List , Optional
from services.fund_service import validate_fund_purchase
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import  Investment
from services.fund_service import NotEnoughUnitsError

router = APIRouter(
    prefix="/funds",
    tags=["funds"]
)

class FundScheme(BaseModel):
    Scheme_Code: int 
    Date: str 
    ISIN_Div_Payout_ISIN_Growth: Optional[str] 
    ISIN_Div_Reinvestment: Optional[str] 
    Mutual_Fund_Family: str 
    Net_Asset_Value: float 
    Scheme_Category: str 
    Scheme_Name: str 
    Scheme_Type: str 
    
class FundResponse(BaseModel):
    funds : List[FundScheme]
    
class PurchaseResponse(BaseModel):
    message: str
    isin: str
    units: int
    scheme_code: int
    scheme_name: str


@router.get("/get_open_schemes",status_code=status.HTTP_200_OK)
async def get_funds(scheme_name: str = None,user_id : dict = Depends(get_user_id)):  
    try:
        if not scheme_name:
            funds_data = get_open_schmes()
        else:
            funds_data = get_open_schmes(scheme_name)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error getting funds"
        )
    print("funds_data:",funds_data)
    funds = [FundScheme(**fund) for fund in funds_data]
    return FundResponse(funds=funds)


@router.post("/invest",status_code=status.HTTP_200_OK)
async def invest(isin: str,units: int,db: Session = Depends(get_db),user_id : dict = Depends(get_user_id)):
    try:
        fund = validate_fund_purchase(isin, units)
    except NotEnoughUnitsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error getting funds"
        )
    print("fund:",fund)        
    investment_obj = (
            db.query(Investment)
            .filter(Investment.user_id == user_id["user_id"], Investment.scheme_code == fund["Scheme_Code"])
            .first()
        )
    print("investment_obj:",investment_obj)
    if not investment_obj:
        investment_obj = Investment(
            user_id=user_id["user_id"],
            scheme_code=fund["Scheme_Code"],
            scheme_name=fund["Scheme_Name"],
            units=units
        )
        db.add(investment_obj)
    else:
        investment_obj.units += units

    db.commit()
    db.refresh(investment_obj)

    return PurchaseResponse(
        message="Purchase successful",
        scheme_code=fund["Scheme_Code"],
        scheme_name=fund["Scheme_Name"],
        units=investment_obj.units
    )