from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .model import User
from .schema import UserCreateModel
from .utils import hash_password, verify_password


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        statement=select(User).where(User.email==email)

        result=await session.exec(statement)

        data=result.first()

        return data


async def create_user(session: AsyncSession, data: UserCreateModel) -> User:
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.exec(select(User))
    return result.all()


async def update_user_role(session: AsyncSession, user_uid, new_role: str) -> User | None:
    user = await session.get(User, user_uid)
    if not user:
        return None
    user.role = new_role
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user