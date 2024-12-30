from agency_swarm import Agent

class EscalationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="EscalationAgent",
            description="Acts as a bridge to human staff for complex or unresolved issues.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=4000
        ) 