#  ______     ______     ______     ______     ______   __     ______     ______    
# /\  ___\   /\  == \   /\  ___\   /\  __ \   /\__  _\ /\ \   /\___  \   /\  ___\   
# \ \ \____  \ \  __<   \ \  __\   \ \  __ \  \/_/\ \/ \ \ \  \/_/  /__  \ \  __\   
#  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\    \ \_\  \ \_\   /\_____\  \ \_____\ 
#   \/_____/   \/_/ /_/   \/_____/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_____/ 

# Licensed under the GNU GPLv3
# meta developer: @visionavtr


from .. import loader, utils

class GovnoSpam(loader.Module):
    """Указывай значения или пойдешь нахуй"""
    strings = {"name": "GovnoSpam", "_cmd_doc_gspamcmd": "<int> <str>"}
    strings_ru = {"_cmd_doc_gspamcmd": "<инт> <стр>"}

    async def gspamcmd(self, message):
        try:
            args=utils.get_args(message)
            await utils.answer(message, "flooding...")
            for _ in range(int(args[0])):
                await client.send_message(message.to_id, " ".join(args[1:]), reply_to=utils.get_topic(message))
            await message.delete()
        except:
            await message.delete()
            return await message.client.send_message(
                message.to_id, "долбоеб, .gspam <инт> и высирай любую хуйню"
            )