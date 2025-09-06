import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file.
# Note: On Render, you will set these as environment variables in the dashboard,
# so the load_dotenv() call is primarily for local development.
load_dotenv() 

class Chatbot:
    def __init__(self):
        # On Render, environment variables are directly available.
        # For local dev, we load them above.
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        # --- CORRECTED PART ---
        # Configure the Google Generative AI library with the API key.
        # This replaces the need for the deprecated genai.Client().
        genai.configure(api_key=api_key)
        
        # Now, get a reference to the model directly.
        # The model name "gemini-2.5-flash" is not a standard public model.
        # The common ones are "gemini-pro" or "gemini-1.5-flash".
        # I'll use "gemini-pro" as an example. You can change this to the correct name.
        self.model = genai.GenerativeModel("gemini-1.5-flash")

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
            # Use the model to generate content directly.
            # No need for self.client.models.generate_content(...)
            response = self.model.generate_content(
                contents=f"{self.system_prompt()}\n\nUser: {user_prompt}"
            )
            return response.text
        except Exception as e:
            return f"❌ Error from Gemini: {str(e)}"