from agency_swarm import Agent
from agency_swarm.tools import FileSearch
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class CustomerInquiryAgent(Agent):
    def __init__(self):
        # Get vector store ID from environment
        self.vector_store_id = os.getenv('VECTOR_STORE_ID')
        if not self.vector_store_id:
            raise ValueError("Vector store ID not found in environment variables")
        
        super().__init__(
            name="CustomerInquiryAgent",
            description="Handles customer questions about order tracking, returns, product information, and FAQs.",
            instructions="./instructions.md",
            tools_folder="./tools",
            tools=[FileSearch],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [self.vector_store_id]
                }
            },
            temperature=0.3,
            max_prompt_tokens=4000
        ) 