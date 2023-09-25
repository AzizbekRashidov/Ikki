import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from scarper import coderun
from sql import Database

db = Database(path_to_db="main.db")
bot = Bot(token='X:X:X:X:X:X:X:X:X', parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
ADMIN = 'X:X:X:X:X:X:X:X:X'



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    botus = await bot.get_me()
    username = botus.username
    if message.chat.type != 'private':
        try:
            db.add_group(user_id=message.chat.id)
        except:pass
        await message.reply(f"""<b>Assalomu alaykum\nMen ishlashim uchun /py commandni yozib ko'ring!</b>""")

    else:
        try:
            db.add_user(user_id=message.from_user.id, name=message.from_user.full_name)
        except:pass
        builder = InlineKeyboardBuilder()
        builder.button(text='• Guruhga qo\'shish •', url=f'https://t.me/PyRun_Bot?startgroup=on&admin=change_info+delete_messages+restrict_members+pin_messages+manage_video_chats+promote_members+invite_users')
        await message.answer(f"""<b>Assalomu alaykum! \n\nMen ishlashim uchun guruhga qo'shing.\n\nGuruhlarda men orqalik python kodlarini ishlatib test qilib ko'rishingiz mumkin!</b>""", reply_markup=builder.as_markup())


@dp.message(Command(commands='py'))
async def command_py_handler(message: Message) -> None:
    botus = await bot.get_me()
    username = botus.username
    if message.chat.type != 'private':
        try:
            db.add_group(user_id=message.chat.id)
        except:pass
        if message.text == "/py":
            await message.answer("""<b>Meni ishlatish uchun:\n\n<code>/py\n\nprint('Salom Dunyo!')</code>\n\nShu kabi kodni yozing!</b>""")
        else:
            result = await coderun(message.text[4:])
            await message.reply(f"""<b>🔰 Output :\n\n<code>{result}</code>\n©️ @{username}</b>""")
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text='• Guruhga qo\'shish •',url=f'https://t.me/PyRun_Bot?startgroup=on&admin=change_info+delete_messages+restrict_members+pin_messages+manage_video_chats+promote_members+invite_users')
        await message.answer("<b>Men faqat guruhda ishlayman!\n\n meni ishlatish uchun guruhga qo'shing:</b>", reply_markup=builder.as_markup())


@dp.message(Command(commands='stat'), lambda message: message.from_user.id == int(ADMIN))
async def command_stat_handler(message: Message) -> None:
    stat = db.stat()
    stat1 = db.stat_group()
    await message.answer(f"Userlar: {stat[0]}\nGuruxlar: {stat1[0]}")
async def main():
    try:
        db.create_table_groups()
        db.create_table_users()
    except:
        pass
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
