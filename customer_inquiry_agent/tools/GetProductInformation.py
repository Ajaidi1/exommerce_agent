from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class GetProductInformation(BaseTool):
    """
    Retrieves product information from the product catalog.
    Requires product ID as input.
    """
    product_id: str = Field(
        ..., description="The product ID to retrieve information for."
    )

    def run(self):
        """
        Implementation of product information retrieval.
        In a production environment, this would integrate with your product catalog system.
        """
        # Mock implementation - in production, replace with actual product catalog integration
        product_catalog = {
            "PROD001": {
                "name": "Premium Wireless Headphones",
                "price": 199.99,
                "description": "High-quality wireless headphones with noise cancellation",
                "stock": 50
            },
            "PROD002": {
                "name": "Smart Watch Pro",
                "price": 299.99,
                "description": "Advanced smartwatch with health monitoring features",
                "stock": 30
            }
        }
        
        if self.product_id in product_catalog:
            product = product_catalog[self.product_id]
            return f"Product Information:\nName: {product['name']}\nPrice: ${product['price']}\nDescription: {product['description']}\nIn Stock: {product['stock']} units"
        else:
            return f"Product {self.product_id} not found in catalog."

if __name__ == "__main__":
    tool = GetProductInformation(product_id="PROD001")
    print(tool.run()) 