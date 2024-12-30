from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class GetFAQ(BaseTool):
    """
    Retrieves the answer to a common question from the FAQ database.
    Requires the question as input.
    """
    question: str = Field(
        ..., description="The question to find an answer for."
    )

    def run(self):
        """
        Implementation of FAQ retrieval.
        In a production environment, this would integrate with your FAQ database.
        """
        # Mock implementation - in production, replace with actual FAQ database integration
        faq_database = {
            "return policy": "You can return any item within 30 days of purchase. Items must be unused and in original packaging.",
            "shipping time": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.",
            "payment methods": "We accept all major credit cards, PayPal, and Apple Pay.",
            "international shipping": "We ship to most countries worldwide. International shipping typically takes 7-14 business days."
        }
        
        # Convert question to lowercase and find best matching key
        question_lower = self.question.lower()
        for key in faq_database:
            if key in question_lower:
                return f"FAQ Answer: {faq_database[key]}"
        
        return "I'm sorry, I couldn't find a specific answer to that question. Please try rephrasing or contact our support team for assistance."

if __name__ == "__main__":
    tool = GetFAQ(question="What is your return policy?")
    print(tool.run()) 