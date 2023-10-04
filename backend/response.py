from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.tools import BaseTool
from typing import Union, Optional
from whisperer import youtube_to_transcription, model
from whisper.model import Whisper

from langchain.tools import BaseTool
from typing import Optional

class YouTubeTranscriptionTool(BaseTool):
    name = "YouTube Transcription"
    description = "This tool transcribes YouTube videos into text using the Whisper ASR model."

    def _run(self, youtube_url: str) -> Optional[str]:
        from whisperer import youtube_to_transcription  # Local import to avoid circular dependencies
        transcribed_text = youtube_to_transcription(youtube_url)
        return transcribed_text or "Transcription failed."

    def _arun(self, youtube_url: str) -> None:
        raise NotImplementedError("This tool does not support async")


youtube_tool = YouTubeTranscriptionTool()

def llm_search_enabled(user_input: str):

    llm = OpenAI(temperature=0)
    # initialize conversational memory
    # conversational_memory = ConversationBufferWindowMemory(memory_key='chat_history', k=5, return_messages=True)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    tools.append(youtube_tool)
    # creating Langchain Agent that uses SERP API to query internet for relevant data
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True) #memory=conversational_memory

    # return LLM output after agent chain completes
    output = agent.run(user_input)

    return output

def llm_search_disabled(user_input: str):

    llm = OpenAI(temperature=0)

    # return LLM output without search
    output = llm.predict(user_input)

    return output