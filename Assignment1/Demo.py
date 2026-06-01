from dotenv import load_dotenv
from litellm import completion
load_dotenv() # reads .env file into environment variables
# Test Gemini
response = completion(
 model="gemini/gemini-2.5-flash",
 messages=[{"role": "user", "content": "Reply with exactly: gemini ok"}],
)
print("Gemini:", response.choices[0].message.content)
# Test Groq
response = completion(
 model="groq/llama-3.3-70b-versatile",
 messages=[{"role": "user", "content": "Reply with exactly: groq ok"}],
)
print("Groq:", response.choices[0].message.content)
