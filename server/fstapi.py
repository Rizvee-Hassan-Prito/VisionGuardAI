from typing import Union
import uvicorn
from fastapi import FastAPI, File, UploadFile
from BLIP import Blip
from Llama import llama
from PIL import Image
import io
import cv2, numpy as np

app = FastAPI()

@app.get("/prompt")
def call_model(prompt: Union[str, None] = 'Hello'):
    reply=llama(prompt)
    return {"reply": reply}

@app.post("/img_to_txt")
async def call_model(img: UploadFile = File(...)):
    contents = await img.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    txt = Blip(image)
    return {"txt": txt}

if __name__ == "__main__":
    uvicorn.run(app, port=80)