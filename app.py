import os
import sys
import requests
from pprint import pprint
sys.stdout.reconfigure(encoding="utf-8")
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
model=init_chat_model(
    model="google_genai:gemini-3.6-flash",
    api_key=gemini_api_key,
)
tavily_api_key=os.getenv("TAVILY_API_KEY")
skill_demand_tool=TavilySearch(
    max_results=5,
    topic="general",
    search_depth="advanced",
    tavily_api_key=tavily_api_key
)
@tool
def search_jobs(skill:str,location:str)->list:
    """Search for jobs requiring a specific skill JSearch API from RapidAPI."""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for:{skill} in {location}")
    rapid_api_key=os.getenv("RAPID_API_KEY")
    url = "https://jsearch.p.rapidapi.com/search-v2"
    querystring = {
        "query": f"{skill} jobs in {location}",
        "num_pages": "1",
        "page": "1",
        "country": "in",
    }
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    jobs = data.get("data", {}).get("jobs", []) ## special to remember
    print(f"Found {len(jobs)} jobs")
    ##pprint(jobs[2])
    result = []
    for job in jobs:
        result.append({
            "title": job.get("job_title", ""),
            "company": job.get("employer_name", ""),
            "location": job.get("job_city", ""),
            "job_description":job.get("job_description",""),
            "apply_link": job.get("job_apply_link", "")
        })
    return result
system_prompt=SYSTEM_PROMPT = """
You are a Skill-to-Career Mapping assistant that helps students understand skill demand,
find matching job opportunities, and identify their skill gaps.

You have access to these tools:
- skill_demand_tool: Research industry demand, salary insights, and career trends
- search_jobs: Find real job listings based on skills and location (includes job
  descriptions and required skills)

Workflow:
1. If the user hasn't told you their current skills yet, ask for them first.
2. Use skill_demand_tool to research what skills are trending for their target role.
3. Use search_jobs to find real openings, and read the 'description' and
   'required_skills' fields returned.
4. Compare the skills mentioned across job listings against the user's stated skills.
5. Present a SKILL GAP section listing: skills the user already has, skills they are
   missing (ranked by how often they appear across listings), and 2-3 concrete next
   steps (courses, projects, certifications) to close the top gaps.

Present results in a clean, readable format with clear sections and spacing.
Include all job details with apply links. Do not use markdown formatting.
"""
checkpointer=InMemorySaver()  ## for saving conversations     
agent=create_agent(
    model=model,
    tools=[skill_demand_tool,search_jobs],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)
config= {
    "configurable": 
    {
    "thread_id":"1",
}
}
user_query="I know Python, LangChain, LangGraph and ChromaDB. What's the demand for generative AI roles and show me jobs in India. What skills am I missing?"
response=agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":user_query
        }
    ]
},config=config)
print(response["messages"][-1].content[0]['text'])
user_query="Which of those jobs is the best match for me, and why?"
response=agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":user_query
        }
    ]
},config=config)
print(response["messages"][-1].content[0]['text'])
user_query="Find jobs in Bengaluru only"
response=agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":user_query
        }
    ]
},config=config)
print(response["messages"][-1].content[0]['text'])
user_query="Give me a 30-day learning plan to close my top 3 missing skills."
response=agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":user_query
        }
    ]
},config=config)
print(response["messages"][-1].content[0]['text'])
     
     

