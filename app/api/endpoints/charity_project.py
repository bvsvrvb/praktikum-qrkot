from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_project_before_delete, check_project_before_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.investment import investment
from app.schemas.charity_project import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.\n
    Создаёт благотворительный проект."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investment.start(new_project, session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть."""
    project = await check_project_exists(
        project_id, session
    )
    check_project_before_delete(project)
    project = await charity_project_crud.remove(
        project, session
    )
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_schema: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной."""

    if obj_schema.name is not None:
        await check_name_duplicate(obj_schema.name, session)

    project = await check_project_exists(
        project_id, session
    )

    check_project_before_update(project, obj_schema.full_amount)

    project = await charity_project_crud.update(
        project, obj_schema, session
    )
    return project
