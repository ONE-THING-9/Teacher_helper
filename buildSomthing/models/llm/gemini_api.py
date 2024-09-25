print("started")
import logging

logging.basicConfig(level=logging.DEBUG)

import google.generativeai as genai
import os

from config import Config

class GeminiModel:
    def get_label(self, prompt:str, model_name:str="gemini-1.5-pro", temp: float=.5, top_p:float=.5, max_tokens:int=512):
        genai.configure(api_key=Config.gemini_api_key)
        
        models = ["gemini-1.5-pro", "gemini-1.5-flash"]
        
        for model_name in models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception as e:
                if model_name == "gemini-1.5-flash":
                    yield f"###error: {e}"
                    return
        
        yield "###error: Both models failed to generate a response."



#