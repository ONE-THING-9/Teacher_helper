import gradio as gr
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def chat_with_llm(user_input, model_name, temperature, top_p, max_tokens):
    url = "http://0.0.0.0:8000/py/llm/chat"
    payload = {
        "user_input": user_input,
        "model_name": model_name,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
    headers = {"Content-Type": "application/json"}

    logger.info(f"Sending request to LLM API with payload: {payload}")
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        logger.info("Successfully received response from LLM API")
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in LLM API request: {str(e)}")
        return f"Error: {str(e)}"

def gradio_interface(user_input, model_name, temperature, top_p, max_tokens):
    logger.info(f"Received input: user_input='{user_input}', model_name={model_name}, temperature={temperature}, top_p={top_p}, max_tokens={max_tokens}")
    response = chat_with_llm(user_input, model_name, temperature, top_p, max_tokens)
    logger.info(f"Generated response: {response[:50]}...")  # Log first 50 characters of the response
    return response

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="User Input"),
        gr.Dropdown(choices=["gemini-1.5-pro"], label="Model Name", value="gemini-1.5-pro"),
        gr.Slider(minimum=0, maximum=1, step=0.1, label="Temperature", value=0.5),
        gr.Slider(minimum=0, maximum=1, step=0.1, label="Top P", value=0.5),
        gr.Slider(minimum=1, maximum=1024, step=1, label="Max Tokens", value=512),
    ],
    outputs="text",
    title="Chat with LLM",
    description="Enter your message and adjust parameters to chat with the LLM.",
)

if __name__ == "__main__":
    logger.info("Starting Gradio interface")
    iface.launch(server_name="0.0.0.0", server_port=8080)
    logger.info("Gradio interface stopped")
