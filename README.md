# Mutual Fund Broker Web Application - FastAPI

## Setup Instructions  
Follow these steps to install and run the application locally:

### Prerequisites  
Ensure the following are installed:
- Python 3.10+
- pip
- Virtual Environment (venv)
- RapidAPI key (to fetch mutual fund data)

### Steps to Setup  
1. **Clone the Repository**
   ```bash
   git clone https://github.com/GunalanD95/mutual-fund-broker-fastapi
   cd mutual-fund-broker-fastapi
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate       # For Linux/Mac
   env\Scripts\activate          # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   - Rename `.env.example` to `.env`.
   - Add your environment variables:
     ```env
     RAPIDAPI_KEY=<your_api_key>
     SECRET_KEY=<your_secret_key>
     ```

5. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at `http://127.0.0.1:8000/`.

6. **Testing the APIs**  
   Use tools like **Postman** or **cURL** to interact with the APIs.

---

## Environment Variables  
The `.env` file must include the following variables:
| Variable           | Description                       |
|--------------------|-----------------------------------|
| `RAPIDAPI_KEY`     | Your RapidAPI API key             |
| `SECRET_KEY`       | JWT SCRET KEY                     |
---------------------------------------------------------
## Running the Application  
1. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Open the Swagger UI for API testing at:
   - `http://127.0.0.1:8000/docs`
   
3. Explore the API documentation for real-time usage and testing.


## API Testing Notes  
- Use `Postman`, `Swagger UI`, or `cURL` to test the APIs.
- Ensure the `RAPIDAPI_KEY` is valid before testing mutual fund APIs.
- Added Postman collection for mutual fund APIs.


