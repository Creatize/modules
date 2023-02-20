#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/cloud_icon.png
# meta banner: https://mods.hikariatama.ru/badges/cloud.jpg
# meta developer: @hikarimods

# scope: hikka_only
# scope: hikka_min 1.2.10

# modified by @penggrin in 2023

import difflib
import inspect
import io
import logging

from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ModuleCloudMod(loader.Module):
    """Hikka Modules Manager, modified by @penggrin"""

    strings = {
        "name": "ModuleCloud",
        "args": "<emoji document_id=5974229895906069525>❓</emoji> <b>Args not specified</b>",
        "404": "<emoji document_id=5974229895906069525>❓</emoji> <b>Module not found</b>",
        "result": '<emoji document_id=5974492756494519709>🔗</emoji> <b><a href="{}">Link</a> for'
    }

    strings_ru = {
        "args": "<emoji document_id=5974229895906069525>❓</emoji> <b>Нет аргументов</b>",
        "404": "<emoji document_id=5974229895906069525>❓</emoji> <b>Модуль не найден</b>",
        "result": '<emoji document_id=5974492756494519709>🔗</emoji> <b><a href="{}">Ссылка</a> на'
    }

    @loader.command(ru_doc="<имя модуля> - Поделиться модулем")
    async def mlcmd(self, message: Message):
        """<module name> - Share a module"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        try:
            try:
                class_name = next(
                    module.strings["name"]
                    for module in self.allmodules.modules
                    if args.lower() == module.strings["name"].lower()
                )
            except Exception:
                try:
                    class_name = next(
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    )
                except Exception:
                    await utils.answer(message, self.strings("404"))
                    return

            module = next(
                filter(
                    lambda mod: class_name.lower() == mod.strings["name"].lower(),
                    self.allmodules.modules,
                )
            )

            sys_module = inspect.getmodule(module)

            link = module.__origin__

            text = (
                f"<emoji document_id=5974492756494519709>🔗</emoji> <b>{utils.escape_html(class_name)}</b>"
                if not utils.check_url(link)
                else (
                    self.strings("result").format(link)
                    + f" {utils.escape_html(class_name)}:</b>"
                    f' <code>{link}</code>\n\n'
                )
            )

            file = io.BytesIO(sys_module.__loader__.data)
            file.name = f"{class_name}.py"
            file.seek(0)

            reply = (await message.get_reply_message()) or utils.get_topic(message) or None
            await message.respond(text, file=file, reply_to=reply)

            if message.out:
                await message.delete()
        except Exception as e:
            logger.error(e)
            await utils.answer(message, self.strings("404"))