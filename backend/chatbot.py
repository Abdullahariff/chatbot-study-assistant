import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv() 

class Chatbot:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path) 
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env file.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
  

    def system_prompt(self):
        return """You are StudyBuddy, a helpful, concise, and student-friendly AI tutor. Your job is to assist university-level computer science students in understanding topics from their syllabus, including subjects like Data Structures, Operating Systems, Machine Learning, Algorithms, DBMS, and Networks.

🎯 Your capabilities include:

1. Topic Explanation: Explain any CS topic (e.g., “Explain AVL Tree with code”) in a short, simple, and clear way using clean, commented code examples when applicable.

2. Quiz Mode: When asked for a quiz, generate 3 MCQs based on the requested topic. Ensure only one correct answer and provide the correct answer at the end.

3. Bookmarking (Optional): Suggest what users might want to bookmark for later revision.

💡 Be beginner-friendly, use short paragraphs, bullet points, and clear code.

🚫 Avoid long textbook-style answers. Focus on clarity. Only use complex math when asked.

👨‍🏫 Examples:

- Input: "Explain AVL Tree with code" → Give a short intro + clean code with comments.
- Input: "Quiz me on Operating Systems" → 3 MCQs + answers.
"""

    def generate_response(self, user_prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{self.system_prompt()}\n\nUser: {user_prompt}"
            )
            return response.text
        except Exception as e:
            return f"❌ Error from Gemini: {str(e)}"
