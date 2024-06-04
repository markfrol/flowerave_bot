from aiogram import types
from sqlalchemy import select
import logging
from db_init import User, Message, get_session
import io


async def add_user(user: types.User):
    try:
        async with get_session() as session:
            result = await session.execute(select(User).filter_by(tg_id=user.id))
            user_db = result.scalar()
            if user_db:
                user_db.username = user.username
                user_db.first_name = user.first_name
                user_db.last_name = user.last_name
                user_db.language_code = user.language_code
            else:
                user_db = User(
                    tg_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    language_code=user.language_code,
                )
                session.add(user_db)
        return True
    except BaseException as err:
        logging.error(f"unexpected error: {err}")
        return False


async def add_message(user: types.User, message: types.Message):
    try:
        async with get_session() as session:
            message_db = Message(user_id=user.id, message_text=message.text)
            session.add(message_db)
        return True
    except BaseException as err:
        logging.error(f"unexpected error: {err}")
        return False


async def send_csv(user_id: int):
    try:
        async with get_session(None) as session:
            messages = await session.execute(select(Message).filter_by(user_id=user_id))
            csv_data = io.StringIO()
            csv_data.write(
                "Дата, Текст сообщения\n",
            )
            for message in messages.scalars().all():
                csv_data.write(f"{message.message_date}, {message.message_text}\n")

            csv_data.seek(0)
            return types.BufferedInputFile(
                file=csv_data.getvalue().encode(), filename="messages.csv"
            )

    except BaseException as err:
        logging.error(f"unexpected error: {err}")
        return False
