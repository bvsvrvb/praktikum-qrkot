from typing import Optional, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return db_project.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, Union[str, float]]]:
        projects = await session.execute(
            select([
                CharityProject.name,
                (func.julianday(CharityProject.close_date) -
                 func.julianday(CharityProject.create_date)
                 ).label('time'),
                CharityProject.description
            ]).where(CharityProject.fully_invested == 1).order_by('time')
        )
        projects = projects.all()

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
