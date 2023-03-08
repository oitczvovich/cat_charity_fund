from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        *,
        project_id: int = None,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Функция ищет проект по имени."""
        db_project = select(CharityProject.id).where(
            CharityProject.name == project_name
        )
        if project_id:
            db_project = db_project.where(
                CharityProject.id != project_id
            )
        project = await session.execute(db_project)
        return project.scalars().first()


charity_project_crub = CRUDCharityProject(CharityProject)
