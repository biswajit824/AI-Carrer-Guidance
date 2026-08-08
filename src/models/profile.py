from pydantic import BaseModel, Field
from typing import List


class StudentProfile(BaseModel):

    name: str = ""

    branch: str

    year: str

    skills: List[str] = Field(default_factory=list)

    projects: List[str] = Field(default_factory=list)

    interests: List[str] = Field(default_factory=list)

    preferred_role: str = ""

    learning_hours_per_day: float = 1.0

    preferred_language: str = "English"

    location_constraint: str = ""