from pydantic import BaseModel


class SwitchAdmin(BaseModel):
    user_id: int


class SwitchIsActive(SwitchAdmin):
    pass
