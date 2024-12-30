from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class ProvideLiveChatOption(BaseTool):
    """
    Informs the customer that a human representative is joining the chat.
    """
    def run(self):
        """
        Implementation of live chat option provision.
        In a production environment, this would integrate with your live chat system.
        """
        # Mock implementation - in production, replace with actual live chat system integration
        chat_id = "CHAT" + str(hash(str(os.urandom(10))))[-6:]
        
        return (
            f"A human representative will be joining this chat shortly.\n"
            f"Chat ID: {chat_id}\n"
            "Please stay in this chat window. Average wait time is 2-3 minutes."
        )

if __name__ == "__main__":
    tool = ProvideLiveChatOption()
    print(tool.run()) 