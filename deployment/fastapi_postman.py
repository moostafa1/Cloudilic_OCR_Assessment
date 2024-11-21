from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from main import image_text_extractor
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/predict")
async def predict_image_caption(file: UploadFile = File(...)):
    try:
        # Check if file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read the image file bytes
        image_bytes = await file.read()

        # Ensure the file is a valid image
        try:
            image = Image.open(BytesIO(image_bytes))
            image.verify()  # Verify the image is valid
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image file: unable to verify image")

        # Generate the caption using image_text_extractor
        try:
            invoice_data = image_text_extractor(image_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Image processing failed: " + str(e))
        
        # Return a JSON response with the extracted caption
        return JSONResponse(content={
            "caption": invoice_data,
            "message": "Image processed successfully"
        })

    except HTTPException as e:
        # If a custom HTTPException is raised, return it as a JSONResponse
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        # Catch any unexpected errors and return a generic error response
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


# uvicorn fastapi_postman:app --reload
