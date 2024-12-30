from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class EscalateTicket(BaseTool):
    """
    Escalates a support ticket to a human representative.
    Requires the conversation summary and priority level.
    """
    conversation_summary: str = Field(
        ..., description="A summary of the conversation so far."
    )
    priority: str = Field(
        ..., description="The priority level of the issue (urgent or non-urgent)."
    )

    def run(self):
        """
        Implementation of ticket escalation.
        In a production environment, this would integrate with your ticketing system.
        """
        # Validate priority level
        if self.priority not in ["urgent", "non-urgent"]:
            return "Invalid priority level. Must be 'urgent' or 'non-urgent'."
        
        # Mock implementation - in production, replace with actual ticketing system integration
        ticket_id = "TKT" + str(hash(self.conversation_summary))[-6:]
        
        response = (
            f"Ticket {ticket_id} has been escalated to our human support team.\n"
            f"Priority Level: {self.priority.upper()}\n"
            f"Conversation Summary: {self.conversation_summary}\n"
            f"A support representative will be assigned to this ticket shortly."
        )
        
        if self.priority == "urgent":
            response += "\nExpected response time: Within 1 hour"
        else:
            response += "\nExpected response time: Within 24 hours"
            
        return response

if __name__ == "__main__":
    tool = EscalateTicket(
        conversation_summary="Customer having issues with order delivery",
        priority="urgent"
    )
    print(tool.run()) 