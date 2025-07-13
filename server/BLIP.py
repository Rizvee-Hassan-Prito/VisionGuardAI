import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


def Blip(raw_image):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    #requests.get(raw_image, stream=True).raw
    #raw_image = Image.open(raw_image).convert('RGB')


    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)

    return processor.decode(out[0], skip_special_tokens=True)


