from utils.logging.logginconfig import setup_logger
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
logging = setup_logger(__name__)

# Configure logging

class OpenAIChat:
    def __init__(self):
        # Fetch the OpenAI API key from the environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            logging.error("API key not found. Ensure it is set in the .env file.")
            raise ValueError("API key not found. Ensure it is set in the .env file.")
        
        # Initialize the OpenAI client with the API key
        self.client = OpenAI(api_key=api_key)
        self.system_message = None
        logging.info("OpenAI client initialized successfully.")




    def set_system_message(self, system_message: str):
        """
        Set the system message that will define the AI's role or behavior.
        """
        self.system_message = system_message
        logging.info(f"System message set to: {system_message}")

    
    
    
    def get_response(self, user_message: str):
        """
        Get a response from the AI based on the user's message and the system's role (if set).
        """
        messages = []
        
        # Include system message if it is set
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
            logging.info(f"System message included in request: {self.system_message}")
        
        # Add the user's message
        messages.append({"role": "user", "content": user_message})
        logging.info(f"User message added: {user_message}")
        
        try:
            # Send the messages to the OpenAI API and get the response
            chat_completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages = messages
                )
            
            # Extract the AI's reply from the response
            ai_response = chat_completion.choices[0].message.content
            
            logging.info(f"AI response received:")
            
            return ai_response, chat_completion.usage.total_tokens
        except Exception as e:
            logging.error(f"Error getting response from OpenAI: {e}")
            raise

