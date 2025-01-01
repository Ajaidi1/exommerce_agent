from agency_swarm import Agent
from agency_swarm.tools import FileSearch
import openai
import os
from dotenv import load_dotenv
#import logging
load_dotenv()
#logging.basicConfig(level=logging.INFO)
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
            max_prompt_tokens=15000
        ) 
#        logging.info(f"CustomerInquiryAgent initialized with tools: {self.tools}")
#    def _run_tool(self, tool_call, message_text):
#        """
#        This function is called when the agent needs to use a tool.
#        """
#        logging.info(f"Running tool: {tool_call.name} with arguments: {tool_call.arguments}")
#        try:
#            return super()._run_tool(tool_call, message_text)
#        except Exception as e:
#            logging.error(f"Error running tool {tool_call.name}: {e}")
#            raise e
#