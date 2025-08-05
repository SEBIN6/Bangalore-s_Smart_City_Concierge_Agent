from agno.agent import Agent
from agno.knowledge import AgentKnowledge
import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file.
load_dotenv()

# Retrieve the OpenRouter API key from the environment variables.
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

if not openrouter_api_key:
    raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file.")


from agno.models.openai import OpenAIChat

class OpenRouterChat(OpenAIChat):
    """
    A custom chat model class for Agno to connect to OpenRouter.
    """
    def __init__(self, id: str, **kwargs):
        super().__init__(
            id=id,
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            **kwargs
        )

# CUSTOM WEB SEARCH TOOL
from agno.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using SerpAPI.
    Use this for current weather, prices, recent events, and up-to-date information.
    """
    if not serpapi_api_key:
        return "Web search is not available. Please add SERPAPI_API_KEY to your .env file."
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": serpapi_api_key,
            "engine": "google"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "organic_results" in data and data["organic_results"]:
            # Extract the first few relevant results
            results = []
            for result in data["organic_results"][:3]:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                results.append(f"Title: {title}\nSnippet: {snippet}")
            
            return f"Search results for '{query}':\n\n" + "\n\n".join(results)
        else:
            return f"No search results found for '{query}'."
            
    except Exception as e:
        return f"Error performing web search: {str(e)}"

# --- PERSONA DETECTION LOGIC ---
def detect_persona(user_input: str, current_persona: str) -> str:
    
    input_lower = user_input.lower()
    
    if "moving here" in input_lower or "work" in input_lower or "live" in input_lower or "neighborhood" in input_lower or "study" in input_lower or "job" in input_lower:
        return "New Resident"
    
    if "weekend trip" in input_lower or "visiting" in input_lower or "see" in input_lower or "attractions" in input_lower or "tour" in input_lower or "explore" in input_lower or "visit" in input_lower or "holiday" in input_lower:
        return "Tourist"
    
    return current_persona
#END OF PERSONA DETECTION

#AGENT SETUP WITH WEB SEARCH TOOL
# Create agent with web search tool
agent = Agent(
    model=OpenRouterChat(id="google/gemini-pro-1.5"),
    tools=[web_search]
)

print("Agent initialized with OpenRouter and web search tool.")

#Create an AgentKnowledge object.
knowledge_base = AgentKnowledge()

# Load the PDF into the AgentKnowledge object.
pdf_path = "The Ultimate Bangalore Guide.pdf" 
try:
    knowledge_base.load_documents([pdf_path])
    print(f"Successfully loaded '{pdf_path}' into the knowledge base.")
except FileNotFoundError:
    print(f"Error: '{pdf_path}' not found. Make sure the file is in the same directory as agent.py.")
except Exception as e:
    print(f"An error occurred while loading the PDF: {e}")

#Set the knowledge base directly on the agent.
agent.knowledge = knowledge_base

print("\nAgent initialized with OpenRouter and knowledge base.")

def run_conversation():
   
    print("\nHello! I am your Bangalore Smart City Concierge. How can I help you today?")
    current_persona = None

    while True:
        user_input = input("\n> You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        detected_persona = detect_persona(user_input, current_persona)
        
        if detected_persona != current_persona:
            current_persona = detected_persona
            if current_persona:
                print(f"Agent: I've detected you are a {current_persona}. I will tailor my responses for you.")
            else:
                print("Agent: I'm not sure if you are a tourist or a resident. Can you tell me a little more about your needs?")

        #System prompt with explicit instructions for blending sources
        system_prompt = "You are a helpful AI concierge for Bangalore."
        system_prompt += " You have access to both a knowledge base from an old city guide and a web search tool for current information."
        system_prompt += " You MUST follow these rules when generating a response:"
        system_prompt += "\n1. Always check your knowledge base (the city guide) first for information. Use the web search tool ONLY for information that could be outdated, such as prices, events, current weather, or new places."
        system_prompt += "\n2. When using information from the PDF, use a phrase like 'According to the city guide...' or 'The city guide mentions...' to cite your source."
        system_prompt += "\n3. When using information from a web search, use a phrase like 'A recent search shows...' or 'Current information indicates...'."
        system_prompt += "\n4. Blend the information from both sources naturally within your response. Do not simply concatenate them."
        system_prompt += "\n5. If information from the PDF conflicts with web search results, acknowledge the conflict (e.g., 'The city guide mentions X, but a recent search shows Y...')."

        if current_persona == "Tourist":
            system_prompt += "\n\nYour user is a visitor to Bangalore (any duration). Be enthusiastic and VERY CONCISE (2-3 sentences max). Focus on top attractions, must-eat places, and Instagram spots. Keep responses short and actionable. DO NOT ask follow-up questions - provide direct, specific recommendations immediately. Adapt recommendations to the time available mentioned by the user."
        elif current_persona == "New Resident":
            system_prompt += "\n\nYour user is a new resident moving for work. Be detailed, practical, and CONCISE (3-4 sentences max). Focus on neighborhoods, cost of living, transportation, and essential services. Provide specific, actionable advice. DO NOT ask follow-up questions - give direct, comprehensive answers immediately."
        else:
             system_prompt += "\n\nThe user's persona is unknown. Ask for more details to understand their needs better."

        try:
            response = agent.run(system_prompt + "\n\nUser: " + user_input)
            print(f"Agent: {response.content}")
        except Exception as e:
            print(f"An error occurred during the conversation: {e}")

run_conversation()