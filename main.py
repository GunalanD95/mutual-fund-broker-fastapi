from fastapi import FastAPI
from database.db import Base, engine
from auth.auth import router as auth_router
from routes.fund_api import router as fund_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(fund_router)

@app.get("/")
def root():
    return {"message": "thank you for traveling with us"}

