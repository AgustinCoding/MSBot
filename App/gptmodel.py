from google import genai
import time

class GPTmodel:

    def __init__(self, api):
        self.client = genai.Client(api_key=api)

    
    def generate_response(self, user_prompt):
        response = self.client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = [user_prompt]
        )
        return response.text