from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.core.config import NULL_VALUE


async def check_not_invested(
    session: AsyncSession,
):
    """
    Получение из БД первых по очереди незакрытых проектов и пожертвований.
    """
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == NULL_VALUE
    ).order_by('create_date'))
    project = project.scalars().first()
    donation = await session.execute(select(Donation).where(
        Donation.fully_invested == NULL_VALUE
    ).order_by('create_date'))
    donation = donation.scalars().first()
    return project, donation


async def investment(
    session: AsyncSession,
    obj,
):
    """Инвестирование пожертвований в проекты."""
    project, donation = await check_not_invested(session)
    if not project or not donation:
        await session.commit()
        await session.refresh(obj)
        return obj
    score_project = project.full_amount - project.invested_amount
    score_donation = donation.full_amount - donation.invested_amount
    if score_project > score_donation:
        project.invested_amount += score_donation
        donation.invested_amount += score_donation
        donation.fully_invested = True
        donation.close_date = datetime.now()
    elif score_project == score_donation:
        project.invested_amount += score_donation
        donation.invested_amount += score_donation
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = datetime.now()
        donation.close_date = datetime.now()
    else:
        project.invested_amount += score_project
        donation.invested_amount += score_project
        project.fully_invested = True
        project.close_date = datetime.now()
    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    return await investment(session, obj)
