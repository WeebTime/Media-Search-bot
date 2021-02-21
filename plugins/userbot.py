import logging
from pyrogram import Client, filters
from info import USERBOT_STRING_SESSION, ADMINS, id_pattern
from utils import save_file

logger = logging.getLogger(__name__)


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files with the help of user bot"""

    if not USERBOT_STRING_SESSION:
        await message.reply('Set `USERBOT_STRING_SESSION` in info.py file or in environment variables.')
    elif len(message.command) == 1:
        await message.reply('Please specify channel username or id in command.\n\n'
                            'Example: `/index -10012345678`')
    else:
        msg = await message.reply('Processing...⏳')
        raw_data = message.command[1:]
        user_bot = Client(USERBOT_STRING_SESSION)
        chats = [int(chat) if id_pattern.search(chat) else chat for chat in raw_data]
        total_files = 0

        try:
            async with user_bot:
                for chat in chats:
                    async for user_message in user_bot.iter_history(chat):
                        message = await bot.get_messages(
                            chat,
                            user_message.message_id,
                            replies=0,
                        )
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                        else:
                            continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Total {total_files} checked!')