# Bangalore Smart City Concierge

An intelligent AI concierge that provides personalized information about Bangalore, India. The agent automatically detects user personas and tailors responses using a hybrid approach combining a knowledge base with real-time web search.

## 🎯 Key Features

### 1. Intelligent Persona Detection

The agent automatically detects whether you're a **tourist** or **new resident** based on your conversation:

**Tourist Detection Keywords:**
- "weekend trip", "visiting", "see", "attractions", "tour", "explore", "visit", "holiday"

**New Resident Detection Keywords:**
- "moving here", "work", "live", "neighborhood", "study", "job"

**How it works:**
```python
def detect_persona(user_input: str, current_persona: str) -> str:
    input_lower = user_input.lower()
    
    # New Resident Detection
    if "moving here" in input_lower or "work" in input_lower or "live" in input_lower:
        return "New Resident"
    
    # Tourist Detection  
    if "weekend trip" in input_lower or "visiting" in input_lower or "attractions" in input_lower:
        return "Tourist"
    
    return current_persona
```

**Response Tailoring:**
- **Tourists**: Enthusiastic, very concise responses (2-3 sentences max) focused on top attractions, must-eat places, and Instagram spots. Direct recommendations without follow-up questions.
- **New Residents**: Detailed, practical, and concise responses (3-4 sentences max) focused on neighborhoods, cost of living, transportation, and essential services. Comprehensive answers without follow-up questions.

### 2. Hybrid Information System: RAG + Web Search

The agent uses a sophisticated decision tree to determine when to use the knowledge base vs. web search:

```
User Query
    ↓
Check Knowledge Base First
    ↓
Is information time-sensitive?
    ├─ YES → Use Web Search
    │   ├─ Current prices
    │   ├─ Weather updates
    │   ├─ Recent events
    │   └─ New places
    │
    └─ NO → Use Knowledge Base
        ├─ Historical facts
        ├─ Established attractions
        ├─ General information
        └─ Cultural context
```

**Decision Criteria:**
- **Use Knowledge Base For**: Historical facts, established attractions, general information, cultural context
- **Use Web Search For**: Current prices, weather, recent events, new places, time-sensitive information

### 3. Creative Features Added

#### A. Smart Source Attribution
The agent provides transparent citations for all information:

- **Knowledge Base**: "According to the city guide..." or "The city guide mentions..."
- **Web Search**: "A recent search shows..." or "Current information indicates..."

#### B. Natural Information Blending
Instead of concatenating sources, the agent naturally blends information:
```
❌ Bad: "The city guide says X. A recent search shows Y."
✅ Good: "While the city guide highlights X as a must-visit spot, 
         current information indicates Y is also gaining popularity 
         among visitors."
```

#### C. Dynamic Persona Adaptation
The agent continuously monitors conversation and adapts its persona:
- Detects persona changes mid-conversation
- Provides feedback when persona is detected: "I've detected you are a Tourist. I will tailor my responses for you."
- Asks clarifying questions when persona is unclear
- Adapts response length and style based on detected persona (concise for tourists, detailed for residents)

### 4. Conflict Resolution System

When information from the knowledge base conflicts with current web search results, the agent:

1. **Acknowledges the conflict explicitly**
2. **Provides both perspectives**
3. **Explains why the difference exists**
4. **Offers the most current information**

**Example Conflict Handling:**
```
"The city guide mentions that entry to Lalbagh Botanical Garden costs ₹20, 
but a recent search shows the current entry fee is ₹50. This increase 
likely reflects recent pricing updates. For the most current information, 
I recommend checking the official website before your visit."
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenRouter API key
- SerpAPI key (optional, for web search)

### Security Note
⚠️ **Important**: Never commit your `.env` file to version control. The `.env.example` file is provided as a template. Your actual API keys should remain private.

### Installation
1. Clone the repository
2. Install dependencies: `pip install agno python-dotenv requests`
3. Set up environment variables:
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Edit `.env` and add your API keys:
     ```
     OPENROUTER_API_KEY=your_openrouter_key
     SERPAPI_API_KEY=your_serpapi_key
     ```
   - Get your OpenRouter API key from: https://openrouter.ai/keys
   - Get your SerpAPI key from: https://serpapi.com/ (optional, for web search)
4. Ensure `The Ultimate Bangalore Guide.pdf` is in the project directory

### Running the Agent
```bash
python agent.py
```

## 🏗️ Architecture

### Core Components

1. **Persona Detection Engine**: Keyword-based classification system
2. **Hybrid Knowledge System**: Combines PDF knowledge base with real-time web search
3. **Response Generator**: Tailored responses based on detected persona
4. **Conflict Resolution**: Handles information discrepancies between sources

### Technology Stack
- **Framework**: Agno (AI agent framework)
- **LLM**: Google Gemini Pro 1.5 (via OpenRouter)
- **Knowledge Base**: PDF document processing
- **Web Search**: SerpAPI with Google search engine
- **Persona Detection**: Custom keyword-based logic

## 📊 Example Interactions

### Tourist Interaction
```
User: "I'm visiting Bangalore for a weekend trip. What should I see?"
Agent: "I've detected you are a Tourist. I will tailor my responses for you.

Perfect! Must-see: Bangalore Palace and Lalbagh Garden. Instagram spots: Cubbon Park and Commercial Street. Try MTR for dosas and Koshy's for dinner!"
```

### New Resident Interaction
```
User: "I'm moving here for work. What neighborhoods should I consider?"
Agent: "I've detected you are a New Resident. I will tailor my responses for you.

Koramangala is perfect for tech professionals - great connectivity, food scene, and 1BHK rents ₹18,000-30,000. Indiranagar is more upscale but expensive. Whitefield offers better value but is further out. Metro connects all areas."
```

## 🔧 Customization

### Adding New Personas
Extend the `detect_persona()` function with new keywords and response patterns.

### Modifying Search Criteria
Adjust the web search decision logic in the system prompt to change when web search is triggered.

### Updating Knowledge Base
Replace `The Ultimate Bangalore Guide.pdf` with any city guide PDF to adapt the agent for different cities.


