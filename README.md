# GPT Chat with Internet Search and YouTube Transcription
## Project Overview
This web application allows users to engage in a conversation with GPT . It offers two unique features: the ability for the model to perform internet searches and transcribe YouTube videos to provide more contextually relevant and informative answers.

## Frontend
Next.js frontend with a minimal UI.

## Backend
Python FastAPI server, that provides 2 API routes: search_enabled and search_disabled.

Search_disabled makes a standard call to GPT3.5.

Search_enabled calls a Langchain Autonomous Agent that is equipped with custom tools to get the task done. Has access to the SERP API for making internet searches, as well as a custom built Youtube Transcription tool that can be used to get the content of a youtube video if that is necessary. Transcription is performed via a locally hosted instance of OpenAI Whisper.

## Setup

The frontend is by default set up on localhost:3000, and can be accessed locally via ```npm run dev```.

The backend is set up on localhost:8000, and can be accessed locally by ```uvicorn main:app --reload``` . :8000/docs contains the swagger documentation for the API routes.

Additionally, OpenAI and SerpAPI keys must be passed into the environment for the API to function.