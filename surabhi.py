import os
from dotenv import load_dotenv
import google.generativeai as genai
import av
import numpy as np
import torch
from transformers import AutoImageProcessor, AutoTokenizer, VisionEncoderDecoderModel
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'json-config.json'
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def image_to_text(image):
  vision_model = genai.GenerativeModel('gemini-pro-vision')
  response = vision_model.generate_content([
    "Can you describe the image",
    image
], stream=True)
  response.resolve()
  print(response.text)
  return response.text

def video_to_text(video):
  # load pretrained processor, tokenizer, and model
  image_processor = AutoImageProcessor.from_pretrained("MCG-NJU/videomae-base")
  tokenizer = AutoTokenizer.from_pretrained("gpt2")
  model = VisionEncoderDecoderModel.from_pretrained("Neleac/timesformer-gpt2-video-captioning").to(device)

  # load video
  container = av.open(video)

  # extract evenly spaced frames from video
  seg_len = container.streams.video[0].frames
  clip_len = model.config.encoder.num_frames
  indices = set(np.linspace(0, seg_len, num=clip_len, endpoint=False).astype(np.int64))
  frames = []
  container.seek(0)
  for i, frame in enumerate(container.decode(video=0)):
      if i in indices:
          frames.append(frame.to_ndarray(format="rgb24"))

 # generate caption
  gen_kwargs = {
      "min_length": 10,
      "max_length": 20,
      "num_beams": 8,
  }
  pixel_values = image_processor(frames, return_tensors="pt").pixel_values.to(device)
  tokens = model.generate(pixel_values, **gen_kwargs)
  caption = tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
  print(caption) # A man and a woman are dancing on a stage in front of a mirror.
  return caption


