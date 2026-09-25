import os
import requests
from typing import Optional, Type, Dict, Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class SkillProofValidationInput(BaseModel):
    agent_id: str = Field(description="The unique identifier of the agent")
    action_hash: str = Field(description="The hash of the action to be validated")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional context for the validation")

class SkillProofValidationTool(BaseTool):
    name: str = "skillproof_behavioral_validation"
    description: str = (
        "Validates an agent's intended behavior using the SkillProof EAS SP-VR validator. "
        "Returns a 402 gasless payment challenge if settlement is required, or the signed attestation."
    )
    args_schema: Type[BaseModel] = SkillProofValidationInput

    def _run(self, agent_id: str, action_hash: str, context: Optional[Dict[str, Any]] = None) -> str:
        api_url = os.environ.get("SKILLPROOF_API_URL", "https://api.nanoempireai.com/v0/validate")
        payload = {
            "agent_id": agent_id,
            "action_hash": action_hash,
            "context": context or {}
        }
        
        try:
            response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 402:
                return f"Payment Required: Please settle the gasless challenge via Biconomy. Details: {response.json()}"
            elif response.status_code == 200:
                return f"Validation Successful: {response.json()}"
            else:
                return f"Validation failed with status {response.status_code}: {response.text}"
        except Exception as e:
            return f"Error connecting to SkillProof validator: {str(e)}"
