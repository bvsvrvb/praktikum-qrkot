from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


class Investment:

    INVEST_TYPE = {
        CharityProject: Donation,
        Donation: CharityProject
    }

    async def get_open_invest_objs(
            self,
            obj_type: Union[CharityProject, Donation],
            session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        """Получение открытых проектов / неинвестированных донатов."""
        db_open_invest_objs = await session.execute(
            select(obj_type).where(
                obj_type.fully_invested == 0
            ).order_by(obj_type.create_date)
        )
        return db_open_invest_objs.scalars().all()

    async def close_obj(
            self,
            obj: Union[CharityProject, Donation]
    ) -> None:
        """Закрытие проекта/доната при полном сборе/исчерпании среств."""
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()
        return None

    async def start(
            self,
            obj_in: Union[CharityProject, Donation],
            session: AsyncSession,
    ) -> None:
        """Распределение нового доната (obj_in - Donation)
        в открытые проекты (invest_obj - CharityProject) или
        Пополнение нового проекта (obj_in - Donation)
        из нераспределенных донатов (invest_obj - CharityProject)"""

        open_invest_objs = await self.get_open_invest_objs(
            self.INVEST_TYPE[type(obj_in)], session
        )

        for invest_obj in open_invest_objs:
            balance_in = obj_in.full_amount - obj_in.invested_amount
            balance_to = invest_obj.full_amount - invest_obj.invested_amount

            if balance_in < balance_to:
                invest_obj.invested_amount += balance_in
                await self.close_obj(obj=obj_in)
            elif balance_in > balance_to:
                obj_in.invested_amount += balance_to
                await self.close_obj(invest_obj)
            else:
                await self.close_obj(obj_in)
                await self.close_obj(invest_obj)

            session.add(invest_obj)
            session.add(obj_in)

        await session.commit()
        await session.refresh(obj_in)
        return None


investment = Investment()
