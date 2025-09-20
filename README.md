# GenAI Weather Agent

A conversational AI assistant that provides real-time weather information for any city using OpenAI's GPT-4o and the wttr.in weather API. The agent follows a step-by-step reasoning process to answer user queries, plan actions, and call tools as needed.

## Features
- Conversational interface for weather queries
- Uses OpenAI GPT-4o for reasoning and planning
- Fetches current weather data from wttr.in
- Extensible tool-based architecture

## Requirements
- Python 3.8+
- OpenAI API key (set in your environment)
- See `requirements.txt` for all dependencies

## Installation
1. Clone this repository:
	```bash
	git clone https://github.com/srishti13722/genai-weather-agent.git
	cd genai-weather-agent
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Set your OpenAI API key in a `.env` file:
	```env
	OPENAI_API_KEY=your_openai_api_key_here
	```

## Usage
Run the agent from your terminal:
```bash
python weather-agent.py
```
You will be prompted to enter a query, such as:
```
> What is the weather in London?
```
The agent will reason step-by-step and return the current weather for the specified city.

## Example Conversation
```
> What is the current weather of New York?
🧠: The user is interested in weather data of new york.
🧠: From the available tools I should call get_weather
🛠️ Tool called : get_weather new york
🤖: The weather for the new york is 12 degrees.
```

## How It Works
- The agent uses a system prompt to guide its reasoning and output format.
- It plans, selects tools, performs actions, observes results, and outputs answers in a structured way.
- The `get_weather` tool fetches weather data for a given city using the wttr.in API.

## Extending
You can add more tools by updating the `available_tools` dictionary in `weather-agent.py`.

## License
MIT License