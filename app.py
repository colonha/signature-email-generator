from fastapi import FastAPI, Form, HTTPException
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Replace this with the URL of your external API
CITIES_API_URL = 'https://64cae5ca700d50e3c70554fa.mockapi.io/api/cities/cities'

@app.get("/")
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/cities")
async def get_cities():
    response = requests.get(CITIES_API_URL)
    if response.status_code == 200:
        cities_data = response.json()
        city_names = [city["name"] for city in cities_data]
        return {"cities": city_names}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch cities.")


@app.post("/generate_email")
async def generate_email(city: str = Form(...)):
    email = f"user@{city.lower().replace(' ', '')}.com"
    return {"email": email}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
