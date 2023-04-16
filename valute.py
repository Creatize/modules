from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


class ValuteMod(loader.Module):
    """Конвертер валют. Edited by @weeldag"""

    strings = {"name": "Valute"}

    async def valcmd(self, message):
        """<сумма> <валюта> - получить курс"""
        state = utils.get_args_raw(message)
        chat = "@exchange_rates_vsk_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1210425892)
                )
                bot_send_message = await message.client.send_message(
                    chat, format(state)
                )
                bot_response = await response
                bot_response_text = bot_response.message.message
                replacements = {
                    "#GloryToUA": "",
                    "https://200rf.com/": "",
                    "======": "",
                    "🇷🇺": "<emoji document_id=6323139226418284334>🇷🇺</emoji> ",
                    "🇧🇾": "<emoji document_id=6323582299539506720>🇧🇾</emoji> ",
                    "🇪🇺": "<emoji document_id=6323217102765295143>🇪🇺</emoji> ",
                    "🇺🇦": "<emoji document_id=6323289850921354919>🇺🇦</emoji> ",
                    "🇺🇸": "<emoji document_id=6323374027985389586>🇺🇸</emoji> ",
                    "🇰🇿": "<emoji document_id=6323135275048371614>🇰🇿</emoji> ",
                    "🇹🇷": "<emoji document_id=6321003171678259486>🇹🇷</emoji> ",
                    "🇺🇿": "<emoji document_id=6323430017179059570>🇺🇿</emoji> ",
                }
                for key, value in replacements.items():
                    bot_response_text = bot_response_text.replace(key, value)

                await bot_send_message.delete()
                await utils.answer(message, f"<b>{bot_response_text.strip()}</b>")
                await bot_response.delete()
            except YouBlockedUserError:
                await utils.answer(message, f"<b>Убери из ЧС:</b> {chat}")
                return
