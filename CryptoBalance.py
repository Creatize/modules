# meta developer: @visionavtr / @toxicuse, @daashhkk
from .. import loader, utils
from telethon.tl.types import Message
cryptobot = 'CryptoBot'
tonrocket = 'tonRocketBot'
xjetswap = 'xJetSwapBot'
cryptotest = 'CryptoTestnetBot'
walletbot = 'wallet'
class CryptoBalanceMod(loader.Module):
	'''Check your balance in some bots.'''
	strings = {'name': 'CryptoBalance', 'balance': '<emoji document_id=5343662197874630855>💲</emoji> <b>Your balance in @{}:</b>\n\n{}'}
	async def check_balance(
		self, 
		bot: int,
		message: Message,
	):
		async with message.client.conversation(bot) as conv:
			enter = await conv.send_message('/wallet')
			otvet = await conv.get_response()
			await enter.delete()
			await otvet.delete()
		return(otvet.text)
	@loader.command()
	async def bcrypto(self, message: Message):
		'''- check your balance in @CryptoBot'''
		balance = ((await self.check_balance(cryptobot, message))[18:]))
		await utils.answer(message, self.strings('balance').format(cryptobot, balance))
	@loader.command()
	async def bton(self, message: Message):
		'''- check your balance in @tonRocketBot'''
		balance = (await self.check_balance(tonrocket, message))[21:]
		await utils.answer(message, self.strings('balance').format(tonrocket, balance))
	@loader.command()
	async def bjet(self, message: Message):
		'''- check your balance in @xJetSwapBot'''
		balance = (await self.check_balance(xjetswap, message))[26:]
		await utils.answer(message, self.strings('balance').format(xjetswap, balance))
	@loader.command()
	async def btest(self, message: Message):
		'''- check your balance in @CryptoTestnetBot'''
		balance = (await self.check_balance(cryptotest, message))[18:]
		await utils.answer(message, self.strings('balance').format(cryptotest, balance))
	@loader.command()
	async def bwallet(self, message: Message):
		'''- check your balance in @wallet'''
		balance = (await self.check_balance(walletbot, message))[22:]
		await utils.answer(message, self.strings('balance').format(walletbot, balance))
