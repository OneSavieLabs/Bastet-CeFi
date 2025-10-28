from typing import List, Literal

from pydantic import BaseModel


class VulnerabilityDetails(BaseModel):
    function_name: str
    description: str
    code_snippet: str


class AuditReport(BaseModel):
    summary: str
    severity: Literal["high", "medium", "low"]
    vulnerability_details: VulnerabilityDetails
    recommendation: str

    def __init__(self, **data):
        data["severity"] = data.get("severity", "").lower()
        if data["severity"] not in ["high", "medium", "low"]:
            data["severity"] = "high"
        super().__init__(**data)
