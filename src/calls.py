from pydantic import BaseModel, Field, validator
from datetime import datetime
import math


class CallAttributes(BaseModel):
    date: str = Field(None, description="UTC date in RFC 3339 format")
    riskScore: float = Field(None,
                             description="number between 0.0 (not risky)  and 1.0 (potential fraud call)",
                             ge=0.0,
                             le=1.0)
    number: str = Field(None, description="phone number in E164 format")
    greenList: bool = Field(None, description="the call is not risky regardless of the risk score")
    redList: bool = Field(None, description="the call is fraud regardless of the risk score")

    @validator('date', allow_reuse=True)
    def check_date_format(cls, value):
        """Make sure date is in RFC 3339 format."""
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            raise ValueError("Incorrect data format, should be RFC 3339 format e.g. 2020-10-12T07:20:50.52Z")
        return value


class Call(BaseModel):
    """
    An object of this class represents an individual phone call with properties type, id and attributes.
    """
    type: str = "call"
    id: str = Field(None, description="Unique Identifier - UUID")
    attributes: CallAttributes


def get_final_risk_score(call: Call):
    """
    Method to combine raw risk score with green/red list status to produce process score.

    The rules for the risk score calculation are:
        - rounded up to 1 DP
        - if on the green list, the value is 0.0
        - if on the red list, the value is 1.0
        - being on the green list has precedence on the red list (e.g. if a call is on the green list and the red list, the risk score will be 0.0)

    :param call: Call object containing risk score, red list and green list attributes

    :return: Final risk score rounded to 1 d.p. [0-1]
    """
    if call.attributes.greenList:
        return 0.0
    elif call.attributes.redList:
        return 1.0
    else:
        return math.ceil(call.attributes.riskScore*10)/10


