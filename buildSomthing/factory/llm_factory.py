from config import Config
from models.llm.gemini_api import GeminiModel

class LLMFActory:
    def get_llm(self, model_name):
        if model_name in Config.gemini_models:
            return GeminiModel()