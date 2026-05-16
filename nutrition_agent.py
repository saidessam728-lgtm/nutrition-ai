import requests
from tavily import TavilyClient

# 1) Tavily API
client = TavilyClient(api_key="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")

# 2) بيانات المستخدم (هنطورها بعدين)
user_input = "وزني 85 كيلو وعايز اخس"

# 3) البحث العلمي
search_result = client.search(
    query="best diet fat loss protein calories research",
    search_depth="advanced"
)

# 4) تجميع المعلومات
research_text = ""

for result in search_result["results"][:3]:
    research_text += result["content"] + "\n\n"

# 5) بناء Prompt للـ AI
prompt = f"""
أنت دكتور تغذية ورياضي محترف.

اعتمد فقط على الأبحاث العلمية التالية:

{research_text}

بيانات المستخدم:
{user_input}

اكتب خطة:
- سعرات حرارية
- بروتين / كارب / دهون
- نظام غذائي بسيط ليوم كامل
- نصيحة تدريب
"""

# 6) إرسال لـ Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }
)

# 7) طباعة النتيجة
print("\n===== AI NUTRITION PLAN =====\n")
print(response.json()["response"])