from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from urllib.request import urlopen, urljoin
import re
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


class ImageExtractionRequest(BaseModel):
    url: str

class ImageExtractionResponse(BaseModel):
    image_urls: List[str]

@app.post("/extract_images", response_model=ImageExtractionResponse)
async def extract_images(request: ImageExtractionRequest):
    try:
        page = urlopen(request.url).read().decode('utf-8')
        img_ex = re.compile('<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
        image_links = img_ex.findall(page)
        image_urls = [urljoin(request.url, src) for src in image_links]
        return ImageExtractionResponse(image_urls=image_urls)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
