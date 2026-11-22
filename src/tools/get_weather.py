from strands.tools import tool

@tool
def get_weather(location: str) -> str:
    """Gets the current weather for a given location."""
    return f"The weather in {location} is currently sunny and 22°C."
