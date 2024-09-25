print("started")
import logging

logging.basicConfig(level=logging.DEBUG)

import google.generativeai as genai
import os

from config import Config



# class GeminiModel:
#     def get_label(prompt:str, model_name:str, temp: float=.5, top_p:float=.5, max_tokens:int=512):
#         pass
# genai.configure(api_key=Config.gemini_api_key)

# model = genai.GenerativeModel(Config.gemini_model)
# print("generation started")
# print(model)
# response = model.generate_content("can you do 2+2")
# print("generation ended")

# print(response)


#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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from router.llm_inference import ChatInput


from router.llm_inference import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Allows all origins
       allow_credentials=True,
       allow_methods=["*"],  # Allows all methods
       allow_headers=["*"],  # Allows all headers
   )

app.include_router(router)
@app.get("/alive")
def alive():
    logging.info("Alive endpoint accessed")
    return {"status": "alive"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
