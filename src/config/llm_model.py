from dotenv import load_dotenv
from strands.models.litellm import LiteLLMModel
import os

load_dotenv()

groq_model = LiteLLMModel(
    model_id="groq/openai/gpt-oss-20b",
    client_args={
        "api_key": os.environ.get("GROQ_API_KEY"),
    },
    params={
        "temperature": 0.7,
        "max_tokens": 1024,
    },
)
