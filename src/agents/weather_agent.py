from dotenv import load_dotenv
from tools.get_weather import get_weather
from strands import Agent
from config.llm_model import groq_model

def weather_agent() -> None:
    load_dotenv()

    agent = Agent(
        model=groq_model,
        tools=[get_weather],
    )
    response = agent("What's the weather like in Paris right now?")
    print(response.structured_output)


if __name__ == "__main__":
    weather_agent()
