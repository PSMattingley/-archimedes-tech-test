from pydantic import BaseModel, Field


class OperatorAttributes(BaseModel):
    prefix: str = Field(None, description="prefix range as 4 digit string int")
    operator: str = Field(None, description="the name of the phone operator")


class Operator(BaseModel):
    """
    An object of this class represents a phone operator with properties type, id and attributes.
    """
    type: str = "operator"
    id: str = Field(None, description="Unique Identifier - UUID")
    attributes: OperatorAttributes




