import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tavily import TavilyClient
from groq import Groq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Tavily Client
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# Groq Client
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# User Data
class UserInput(BaseModel):
    weight: int
    height: int
    age: int
    goal: str


@app.get("/")
def home():
    return {"message": "Nutrition AI API Running"}


@app.post("/analyze")
def analyze(user: UserInput):

    # Search Research
    search_result = tavily_client.search(
        query=f"nutrition diet {user.goal} protein calories research",
        search_depth="advanced"
    )

    # Collect Research
    research_text = ""

    for r in search_result["results"][:2]:
        research_text += r["content"] + "\n\n"

    # AI Prompt
    prompt = f"""
أنت دكتور تغذية محترف.

اعتمد على الأبحاث التالية:

{research_text}

بيانات المستخدم:
- الوزن: {user.weight}
- الطول: {user.height}
- العمر: {user.age}
- الهدف: {user.goal}

قم بإنشاء:
1- السعرات اليومية
2- البروتين والكارب والدهون
3- نظام غذائي يومي
4- نصائح تدريب
5- نصائح صحية
"""

    # AI Response
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-8b-instant"
    )

    result = chat_completion.choices[0].message.content

    return {
        "result": result
    }