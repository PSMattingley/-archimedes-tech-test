from pydantic import BaseModel, Field, validator
from datetime import datetime
import math


class CallAttributes(BaseModel):
    date: str = Field(None, description="UTC date in RFC 3339 format")
    riskScore: float = Field(None,
                             description="number between 0.0 (not risky)  and 1.0 (potential fraud call)",
                             ge=0.0,
                             le=1.0)
    number: str = Field("Withheld", description="phone number in E164 format")
    greenList: bool = Field(None, description="the call is not risky regardless of the risk score")
    redList: bool = Field(None, description="the call is fraud regardless of the risk score")

    @validator('date', allow_reuse=True)
    def check_date_format(cls, value):
        """Make sure date is in RFC 3339 format."""
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError("Incorrect data format, should be RFC 3339 format e.g. 2020-10-12T07:20:50.52Z")
        return value

    def get_operator_prefix(self):
        """
        :return: Operator code extacted from the number or None
        """
        if self.number == "Withheld":
            return 'Unknown'
        else:
            return self.number[3]+'000'

    def get_short_date(self):
        """
        return: The date as YYYY-MM-DD format
        """
        return self.date.split('T')[0]


class Call(BaseModel):
    """
    An object of this class represents an individual phone call with properties type, id and attributes.
    """
    type: str = "call"
    id: str = Field(None, description="Unique Identifier - UUID")
    attributes: CallAttributes

    def get_report_dict(self):
        return {'id': self.id,
                'date': self.attributes.get_short_date(),
                'number': self.attributes.number,
                'operator_prefix': self.attributes.get_operator_prefix(),
                'riskScore': self.get_final_risk_score()}

    def get_final_risk_score(self):
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
        if self.attributes.greenList:
            return 0.0
        elif self.attributes.redList:
            return 1.0
        else:
            return math.ceil(self.attributes.riskScore * 10) / 10
