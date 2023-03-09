#  ______     ______     ______     ______     ______   __     ______     ______    
# /\  ___\   /\  == \   /\  ___\   /\  __ \   /\__  _\ /\ \   /\___  \   /\  ___\   
# \ \ \____  \ \  __<   \ \  __\   \ \  __ \  \/_/\ \/ \ \ \  \/_/  /__  \ \  __\   
#  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\    \ \_\  \ \_\   /\_____\  \ \_____\ 
#   \/_____/   \/_/ /_/   \/_____/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_____/ 

# Licensed under the GNU GPLv3
# requires: math sympy mpmath
# meta developer: @visionavtr, @daffmaybe
# special thanks to @daffmaybe

from .. import loader, utils 
from math import sqrt, factorial, sin, cos, tan, radians 
from sympy import subfactorial 
  
class Calcmod(loader.Module): 
    strings = {"name": "Extended calc", "_cls_doc": " Calculator with many functions. Only .e is better", "err_txt": "<b>[Calc]</b> Error in a case"}
    strings_ru = {"_cls_doc": " Калькулятор со множеством функций. Лучше только .e", "err_txt": "<b>[Calc]</b> Ошибка в примере"}
    
 
    async def clcmd(self, message): 
        """- ваш пример""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"{args} = <code>{eval(args)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def fctcmd(self, message): 
        """- вычисляет факториал числа""" 
        args = utils.get_args_raw(message) 
        try:
            await utils.answer(message, f"{args}! = <code>{round(factorial(int(args)), 5)}</code>") 
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def sqrtcmd(self, message): 
        """- вычисляет квадратный корень числа""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"√{args} = <code>{round(sqrt(float(args)), 5)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def sfctcmd(self, message): 
        """- вычисляет субфакториал числа""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"!{args} = <code>{round(subfactorial(int(args)), 5)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def coscmd(self, message): 
        """- вычисляет косинус числа""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"cos({args}) = <code>{round(cos(radians(float(args))), 5)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def sincmd(self, message): 
        """- вычисляет синус числа""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"sin({args}) = <code>{round(sin(radians(float(args))), 5)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
 
    async def tancmd(self, message): 
        """- вычисляет тангенс числа""" 
        args = utils.get_args_raw(message)
        try:
            await utils.answer(message, f"tg({args}) = <code>{round(tan(radians(float(args))), 5)}</code>")
        except:
            await utils.answer(message, self.strings("err_txt"))
