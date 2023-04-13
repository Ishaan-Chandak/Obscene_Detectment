from fastapi import FastAPI
import numpy as np
import requests
from PIL import Image, ImageFile
import torch
from transformers import AutoModelForImageClassification, AutoFeatureExtractor
import io
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Input(BaseModel):
    image_url: str

class Output(BaseModel):
    predictions: str

@app.post("/predict", response_model=Output)
def predict(input: Input):
    # Download the image from the URL
    response = requests.get(input.image_url)
    image = Image.open(io.BytesIO(response.content)).convert('RGB')

    # Resize the image to match the input size expected by the model
    size = (224, 224)
    image = image.resize(size)
    image.save('output.png')

    # Convert the image to a NumPy array
    data = np.asarray(image)
    data = np.expand_dims(data, axis=0)

    feature_extractor = AutoFeatureExtractor.from_pretrained('vit-base-patch16-224-hentai')
    model = AutoModelForImageClassification.from_pretrained('vit-base-patch16-224-hentai')

    # prepare image for the model
    encoding = feature_extractor(image.convert("RGB"), return_tensors="pt")
    print(encoding.pixel_values.shape)

    # forward pass
    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()
    # Return the predictions
    return {"predictions": model.config.id2label[predicted_class_idx]}

if __name__ == "__main__":
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    uvicorn.run(app, host="0.0.0.0", port=8000)
