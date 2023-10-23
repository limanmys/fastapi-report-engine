from pydantic import BaseModel, Field
import typing

class ReportCreateRequest(BaseModel):
    Data: typing.List[typing.Dict[str,typing.Any]] = Field(default_factory=list, alias="data")
    Columns: typing.List[str] = Field(default_factory=list, alias="columns")
    Header: str = Field(alias="header")
    Date: str = Field(alias="date")
    TemplateID: str = Field(alias="template_id")
