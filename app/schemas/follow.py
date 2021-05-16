from pydantic import BaseModel


class ChangeFollowStatus(BaseModel):
    album_id: int
    last_ep: int
