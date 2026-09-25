# SkillProof Validation Tool

Validates agent actions via the Nano Empire SkillProof EAS SP-VR validator with gasless x402 payments on Base.

## Installation
```bash
pip install langchain-community
```

## Usage
```python
from langchain_community.tools.skillproof import SkillProofValidationTool

tool = SkillProofValidationTool()
result = tool._run(
    agent_id="my-agent-001",
    action_hash="0x1234...",
    context={"chain": "base", "action_type": "transfer"}
)
print(result)
```

## Environment Variables
- `SKILLPROOF_API_URL` - Override default endpoint (default: https://api.nanoempireai.com/v0/validate)
