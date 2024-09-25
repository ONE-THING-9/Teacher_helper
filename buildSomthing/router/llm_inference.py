from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from models.llm.gemini_api import GeminiModel
from prompt_formater import render_jinja_template
from config import Config
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatInput(BaseModel):
    topic: str
    subject: str
    knowledge_level: str
    include_numerical_questions: bool
    class_level: str
    model_name: str = Config.gemini_models[0]
    temperature: float = 0.5
    top_p: float = 0.5
    max_tokens: int = 512

@router.post("/py/llm/chat")
async def chat_with_gemini(chat_input: ChatInput):
    """
    FastAPI endpoint to chat with the Gemini model and stream the response.
    """
    logger.info(f"Received chat request")

    def generate():
        try:
            with open("prompts/teach.text", "r") as f:
                template = f.read()
            placeholder = {
                "subject": chat_input.subject,
                "topic": chat_input.topic,
                "knowledge_level": chat_input.knowledge_level,
                "include_numerical_questions": chat_input.include_numerical_questions,
                "class_level": chat_input.class_level
            }
            final_prompt = render_jinja_template(template, placeholder)
            logger.info(f"Final prompt: {final_prompt}")
            gemini_model = GeminiModel()
            logger.info(f"Using model: {chat_input.model_name}")
            for token in gemini_model.get_label(
                prompt=final_prompt,
                model_name=chat_input.model_name,
                temp=chat_input.temperature,
                top_p=chat_input.top_p,
                max_tokens=chat_input.max_tokens
            ):
                yield f"{token}"
            
            logger.info("Successfully streamed response from Gemini model")
        except Exception as e:
            logger.error(f"Error in chat_with_gemini: {str(e)}", exc_info=True)
            yield f"data: ERROR: {str(e)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
