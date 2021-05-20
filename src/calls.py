from pydantic import BaseModel, Field


class CallAttributes(BaseModel):
    date: str = Field(None, description="UTC date in RFC 3339 format")
    riskScore: float = Field(None,
                             description="number between 0.0 (not risky)  and 1.0 (potential fraud call)",
                             ge=0.0,
                             le=1.0)
    number: str = Field(None, description="phone number in E164 format")
    greenList: bool = Field(None, description="the call is not risky regardless of the risk score")
    redList: bool = Field(None, description="the call is fraud regardless of the risk score")


class Call(BaseModel):
    """
    An object of this class represents an individual phone call with properties type, id and attributes.
    """
    type: str = "call"
    id: str = Field(None, description="Unique Identifier - UUID")
    attributes: CallAttributes





