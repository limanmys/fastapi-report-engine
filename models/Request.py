from pydantic import BaseModel, Field
from typing import Dict
import typing

class ReportCreateRequest(BaseModel):
    Data: list[Dict[str,typing.Any]] = Field(default_factory=list, alias="data")
    Columns: list[str] = Field(default_factory=list, alias="columns")
    Header: str = Field(alias="header")
    Date: str = Field(alias="date")
    TemplateID: str = Field(alias="template_id")
