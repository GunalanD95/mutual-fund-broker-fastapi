from fastapi import APIRouter, Depends, HTTPException, status
from services.fund_service import get_open_schmes 
from auth.jwt import get_user_id
from pydantic import BaseModel
from typing import List , Optional
from services.fund_service import validate_fund_purchase
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import  Investment , User , Fund
from services.fund_service import NotEnoughUnitsError

router = APIRouter(
    prefix="/funds",
    tags=["funds"]
)

class FundScheme(BaseModel):
    scheme_code: int  
    scheme_name: str 
    nav: float 
    scheme_type: Optional[str] = None 
    scheme_category: Optional[str] = None 

    class Config:
        orm_mode = True 

    
class FundResponse(BaseModel):
    funds : List[FundScheme]

class PortfolioItem(BaseModel):
    scheme_code: str
    scheme_name: str
    nav : float
    units: float


class PortfolioResponse(BaseModel):
    user_id: int
    portfolio: List[PortfolioItem]


@router.get("/get_open_schemes",status_code=status.HTTP_200_OK)
async def get_funds(scheme_name: str = None,user_id : dict = Depends(get_user_id),db: Session = Depends(get_db)):  
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
    funds = []
    for fund in funds_data:
        funds.append(FundScheme(
            scheme_code=fund["Scheme_Code"],
            scheme_name=fund["Scheme_Name"],
            nav=fund["Net_Asset_Value"],
            scheme_type=fund["Scheme_Type"],
            scheme_category=fund["Scheme_Category"]
        ))
        fund_obj = db.query(Fund).filter(Fund.scheme_code == fund["Scheme_Code"]).first()
        if not fund_obj:
            new_fund = Fund(
                scheme_code=fund["Scheme_Code"],
                scheme_name=fund["Scheme_Name"],
                nav=fund["Net_Asset_Value"],
                scheme_type=fund["Scheme_Type"],
                scheme_category=fund["Scheme_Category"]
            )
            db.add(new_fund)
    db.commit()
    return FundResponse(funds=funds)


@router.post("/invest",status_code=status.HTTP_200_OK)
async def invest(
    isin: str,
    units: str,
    db: Session = Depends(get_db),
    user_id: dict = Depends(get_user_id)
):
    try:
        fund = validate_fund_purchase(isin, float(units))
    except NotEnoughUnitsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough units to invest"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error fetching or validating fund details"
        )

    investment_obj = (
        db.query(Investment)
        .filter(Investment.user_id == user_id["user_id"], Investment.scheme_code == fund["Scheme_Code"])
        .first()
    )

    if not investment_obj:
        investment_obj = Investment(
            user_id=user_id["user_id"],
            scheme_code=fund["Scheme_Code"],
            units=float(units),
            total_value=0 # TODO: calculate total value
        )                
        db.add(investment_obj)
    else:
        investment_obj.units += float(units)
        
    db.commit()
    db.refresh(investment_obj)
    return {
        "message": "Investment successful",
        "scheme_code": fund["Scheme_Code"],}
    
@router.get("/portfolio", response_model=PortfolioResponse, status_code=status.HTTP_200_OK)
async def get_portfolio(
    db: Session = Depends(get_db),
    user_id: dict = Depends(get_user_id)
):
    user_obj = db.query(User).filter(User.id == user_id["user_id"]).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    investments = db.query(Investment).filter(Investment.user_id == user_id["user_id"]).all()
    if not investments:
        raise HTTPException(status_code=404, detail="No investments found in portfolio")

    portfolio_items = []
    for investment in investments:
        fund = db.query(Fund).filter(Fund.scheme_code == investment.scheme_code).first()
        if not fund:
            raise HTTPException(status_code=404, detail="Fund not found")
        portfolio_items.append(PortfolioItem(
            scheme_code=fund.scheme_code,
            scheme_name=fund.scheme_name,
            nav=fund.nav,
            units=investment.units
        ))
    return PortfolioResponse(user_id=user_id["user_id"], portfolio=portfolio_items)

