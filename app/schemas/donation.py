from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint


class DonationCreate(BaseModel):
    full_amount: conint(strict=True, gt=0)
    comment: Optional[str]


class DonationDBshort(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationDBshort):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
