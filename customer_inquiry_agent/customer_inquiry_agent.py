from agency_swarm import Agent
from agency_swarm.tools import FileSearch

class CustomerInquiryAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CustomerInquiryAgent",
            description="Handles customer questions about order tracking, returns, product information, and FAQs.",
            instructions="./instructions.md",
            tools_folder="./tools",
            tools=[FileSearch],
            temperature=0.3,
            max_prompt_tokens=4000
        ) 