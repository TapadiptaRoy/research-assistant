# Quick manual check: confirms config.py loads correctly and Claude responds

from langchain_anthropic import ChatAnthropic
from config import ANTHROPIC_API_KEY

llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=ANTHROPIC_API_KEY)

response = llm.invoke("Say hello in one sentence.")

print(response.content)