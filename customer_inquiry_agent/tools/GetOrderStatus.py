from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class GetOrderStatus(BaseTool):
    """
    Retrieves order status from the order management system.
    Requires the order ID as input.
    """
    order_id: str = Field(
        ..., description="The order ID to retrieve status for."
    )

    def run(self):
        """
        Implementation of the order status retrieval.
        In a production environment, this would integrate with your actual order management system.
        """
        # Mock implementation - in production, replace with actual CRM integration
        order_statuses = {
            "ORD123": "Shipped - Expected delivery on 2024-01-20",
            "ORD124": "Processing - Will ship within 24 hours",
            "ORD125": "Delivered on 2024-01-15"
        }
        
        if self.order_id in order_statuses:
            return f"Order Status for {self.order_id}: {order_statuses[self.order_id]}"
        else:
            return f"Order {self.order_id} not found in the system."

if __name__ == "__main__":
    tool = GetOrderStatus(order_id="ORD123")
    print(tool.run()) 