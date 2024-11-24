from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import base64
from PIL import Image
from main import image_text_extractor
from config import CONFIG



# Create FastAPI instance
app = FastAPI()

# Serve the static files (like images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def welcome_page(request: Request):
    try:
        return templates.TemplateResponse("welcome.html", {"request": request})
    except Exception as e:
        # Catching unexpected errors and returning a JSON response
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@app.post("/predict", response_class=HTMLResponse)
async def predict_image_caption(request: Request, file: UploadFile = File(...)):
    try:
        if file is None:
            raise HTTPException(status_code=400, detail="No file provided")

        image_bytes = await file.read()

        # Check if the file is a valid image (optional)
        try:
            image = Image.open(BytesIO(image_bytes))
            image.verify()  # Verify the image is valid
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Generate the caption using your custom image_text_extractor
        invoice_data = image_text_extractor(image_bytes)

        # Convert the image bytes to a base64 string to display in the HTML
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_src = f"data:image/jpeg;base64,{image_base64}"

        return templates.TemplateResponse("result.html", {
            "request": request,
            "caption": invoice_data[1:-1].replace('"', '').replace(",", "<br>"),
            "image_src": image_src
        })

    except HTTPException as e:
        # Handle the HTTP exceptions such as missing files or invalid images
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        # Catch unexpected errors and return a general error response
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


# uvicorn fastapi_deployment:app --reload
