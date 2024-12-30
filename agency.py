from agency_swarm import Agency
from agency_swarm import set_openai_key
from customer_inquiry_agent.customer_inquiry_agent import CustomerInquiryAgent
from escalation_agent.escalation_agent import EscalationAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
set_openai_key(os.getenv('OPENAI_API_KEY'))

# Initialize agents
customer_inquiry = CustomerInquiryAgent()
escalation = EscalationAgent()

# Create agency with communication flows
agency = Agency(
    [
        customer_inquiry,  # CustomerInquiryAgent will be the entry point
        [customer_inquiry, escalation],  # CustomerInquiryAgent can communicate with EscalationAgent
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.3,
    max_prompt_tokens=4000
)

if __name__ == "__main__":
    agency.run_demo()  # Start the agency in terminal mode 