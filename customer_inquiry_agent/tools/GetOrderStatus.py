from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access Shopify API credentials from environment variables
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")

class GetOrderStatus(BaseTool):
    """
    Retrieves order status from Shopify using the Shopify Admin API.
    """
    order_id: str = Field(
        ..., description="The Shopify order ID or order name (e.g., 1001 or #1001) to retrieve the status for. "
    )

    def run(self):
        """
        Makes a request to the Shopify Admin API to get order details and returns the status.
        """
        headers = {
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json",
        }

        # Check if the input looks like an order name (e.g., #1001)
        if self.order_id.startswith("#"):
            # If it's an order name, remove the # and search by name
            order_name = self.order_id[1:]
            url = f"https://{SHOPIFY_STORE_URL}/admin/api/2023-10/orders.json?name={order_name}"
        else:
            # Otherwise, assume it's an order ID
            url = f"https://{SHOPIFY_STORE_URL}/admin/api/2023-10/orders/{self.order_id}.json"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()


            # If searching by name, the response will contain a list of orders
            order_data = response.json()
            if 'orders' in order_data:
                orders = order_data['orders']
                if orders:
                    # Assuming the first order in the list is the one we want
                    order_data = orders[0]
                else:
                    return f"Order {self.order_id} not found in the Shopify store."
            else:
                # If searching by ID, the response will contain a single order
                order_data = order_data.get("order")

            if order_data:
                order_number = order_data.get("name", "Not available")
                created_at = order_data.get("created_at", "Not available")
                financial_status = order_data.get("financial_status", "Not available")
                fulfillment_status = order_data.get("fulfillment_status", "Not available")

                # Extract tracking URL (from the first fulfillment, if available)
                tracking_url = "Not available"
                tracking_company = "Not available"
                tracking_number = "Not available"
                fulfillments = order_data.get("fulfillments", [])
                if fulfillments:
                    fulfillment = fulfillments[0]  # Get the first fulfillment
                    tracking_url = fulfillment.get("tracking_url", "Not available")
                    tracking_company = fulfillment.get("tracking_company", "Not available")
                    tracking_number = fulfillment.get("tracking_number", "Not available")

                # Extract tags
                tags = order_data.get("tags", "No tags")

                # Format the date and time
                if created_at != "Not available":
                    # Format the date and time to be more user-friendly
                    from datetime import datetime
                    date_time_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S%z")
                    created_at = date_time_obj.strftime("%B %d, %Y at %I:%M %p")

                status_message = (
                    f"Order Status for {order_number}:\n\n"
                    f"Created at: {created_at}\n"
                    f"Financial Status: {financial_status}\n"
                    f"Fulfillment Status: {fulfillment_status}\n"
                    f"Shipping Information:\n"
                    f"    Tracking Company: {tracking_company}\n"
                    f"    Tracking Number: {tracking_number}\n"
                    f"    Tracking URL: {tracking_url}\n"
                    f"Tags: {tags}\n"
                )

                return status_message
            else:
                return f"Order {self.order_id} not found in the Shopify store."

        except requests.exceptions.RequestException as e:
            return f"Error accessing Shopify API: {e}"

if __name__ == "__main__":
    # For testing purposes, create a test order in your Shopify dev store to get a real order ID
    # Replace "your_order_id" with an actual order ID or order name (e.g., "5432109876543" or "#1001") from your store
    tool = GetOrderStatus(order_id="#1001")  # Replace with an actual order ID or order name
    print(tool.run())
