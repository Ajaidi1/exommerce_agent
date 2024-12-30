from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class ProvideCallbackOption(BaseTool):
    """
    Provides the customer with a callback option.
    """
    def run(self):
        """
        Implementation of callback option provision.
        In a production environment, this would integrate with your callback scheduling system.
        """
        # Mock implementation - in production, replace with actual callback system integration
        callback_id = "CB" + str(hash(str(os.urandom(10))))[-6:]
        
        return (
            "We can have a support representative call you back.\n"
            f"Callback Reference: {callback_id}\n"
            "Our support team operates from 9 AM to 6 PM EST, Monday through Friday.\n"
            "You will receive a call within the next business hour."
        )

if __name__ == "__main__":
    tool = ProvideCallbackOption()
    print(tool.run()) 