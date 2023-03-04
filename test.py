from .. import loader, utils

strings = {"name": "NoobHelper"}

class sometestMod(loader.Module):
    """Test Module"""

    async def testcmd(self, message):
                await utils.answer("test")
                return