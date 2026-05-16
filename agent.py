```python id="n1"
import requests
from tavily import TavilyClient

# Tavily API Key
client = TavilyClient(
    api_key="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"
)

# البحث العلمي
search_result = client.search(
    query="best protein intake for muscle growth",
    search_depth="advanced"
)

# تجميع نتائج الأبحاث
research_text = ""

for result in search_result["results"][:3]:
    research_text += result["content"] + "\n\n"

# البرومبت النهائي
prompt = f"""
أنت دكتور تغذية محترف ومتخصص في التغذية الرياضية.

اعتمد فقط على الأبحاث العلمية التالية:

{research_text}

قم بشرح:
- أفضل كمية بروتين لبناء العضلات
- أفضل توقيت للبروتين
- أهمية البروتين بعد التمرين
- نصائح عملية للمبتدئين

اجعل الشرح بسيط وواضح.
"""

# إرسال البرومبت إلى Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }
)

# تحويل الرد إلى JSON
result = response.json()

# عرض النتيجة
if "response" in result:
    print("\n===== AI RESPONSE =====\n")
    print(result["response"])
else:
    print("\n===== ERROR =====\n")
    print(result)
```
