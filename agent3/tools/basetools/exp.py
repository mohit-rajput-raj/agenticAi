from typing import Any, Dict, Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class GetWeatherTool(BaseTool):
    # Annotate these fields
    name: str = "get_weather"
    description: str = "Get the current weather for a city."
    
    # It is recommended to use pydantic.Field for args_schema in modern LangChain
    args_schema: Optional[Type[BaseModel]] = None 

    def _run(self, city: str) -> str:
        """Execute the tool."""
        return f"Sunny in {city}"

    async def _arun(self, city: str) -> str:
        """Async execution (optional)."""
        return f"Sunny in {city}"

# Create and use the tool
weather_tool = GetWeatherTool()
print(weather_tool.invoke({"city": "Paris"}))