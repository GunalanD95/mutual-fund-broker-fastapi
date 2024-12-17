import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("RAPIDAPI_KEY")
API_HOST = "latest-mutual-fund-nav.p.rapidapi.com"
BASE_URL = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"


def get_open_schmes(fund_family : str = None):
    querystring = {"Scheme_Type":"Open"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    if fund_family:
        querystring["Mutual_Fund_Family"] = fund_family
    response = requests.get(BASE_URL, headers=headers, params=querystring)
    if response.status_code != 200:
        print("error status_code:", response.status_code, "error message:", response.text)
        raise Exception("Error getting funds")
    return response.json()

def fetch_fund_details(isin: str):
    URL = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"

    querystring = {"ISIN": isin}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(URL, headers=headers, params=querystring)
    if response.status_code != 200:
        print("error status_code:", response.status_code, "error message:", response.text)
        raise Exception("Error getting funds")
    print("response:", response.json())
    return response.json()


class NotEnoughUnitsError(Exception):
    pass

def validate_fund_purchase(isin: str, units: int):
    fund_data = fetch_fund_details(isin)
    print("fund_data:",fund_data)
    for fund in fund_data:
        if not fund.get("Purchase_Allowed"):
            raise ValueError("Purchase is not allowed for this fund")

        if int(units) < fund.get("Minimum_Purchase_Amount", 0):
            raise NotEnoughUnitsError(
                f"Minimum purchase amount is {fund['Minimum_Purchase_Amount']} units"
            )
        return fund  
    raise ValueError("No fund found matching the provided ISIN")
