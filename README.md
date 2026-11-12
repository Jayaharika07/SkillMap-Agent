# SkillMap – AI Career & Skill-Gap Advisor

## Project Overview
SkillMap is an AI-powered career guidance assistant that helps users understand industry skill demand, discover relevant job opportunities, identify missing skills, and create personalized learning plans.

## Features
- Researches trending skills and industry demand using Tavily Search.
- Finds relevant job opportunities using JSearch API.
- Analyzes job descriptions and required skills.
- Identifies skill gaps based on the user's existing skills.
- Provides personalized career and learning recommendations.
- Maintains conversational context using LangGraph memory.

## Technologies Used
- Python
- LangChain
- LangGraph
- Google Gemini
- Tavily Search API
- JSearch API (RapidAPI)
- Requests
- Python-dotenv

## Installation

1. Clone the repository.
2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Create a `.env` file and configure your API keys.

## Run the Project

`python main.py`

## Environment Variables

- GEMINI_API_KEY
- TAVILY_API_KEY
- RAPID_API_KEY

## Project Status
Developed as an AI-powered career and skill-gap analysis assistant.

## Author
M. Jaya Harika