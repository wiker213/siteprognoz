from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Dict, List, Optional


class CalculationInput(BaseModel):
    indicator: str = Field(..., description="Код показателя (vrp_production, inflation, etc.)")
    data: Dict[str, float] = Field(default_factory=dict)


class ForecastInput(BaseModel):
    method: str = Field(..., description="average | moving | holt")
    values: List[float] = Field(..., min_length=1)
    horizon: int = Field(..., ge=1, le=120)


class RegionInfo(BaseModel):
    name: str
    area_km2: float
    population: int
    vrp: Optional[float] = None
    industries: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class UpdatesInfo(BaseModel):
    last_update: str
    changed_indicators: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip().lower()

        if not re.fullmatch(r"[a-zA-Z0-9_]+", value):
            raise ValueError("Логин может содержать только латинские буквы, цифры и _")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()

        if "@" not in value or "." not in value:
            raise ValueError("Некорректный email")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(ch.isdigit() for ch in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")

        if not any(ch.isalpha() for ch in value):
            raise ValueError("Пароль должен содержать хотя бы одну букву")

        return value


class UserLogin(BaseModel):
    login: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    is_active: bool