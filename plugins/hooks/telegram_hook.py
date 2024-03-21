import asyncio
from airflow.hooks.base import BaseHook
from telegram import Bot


class TelegramBotHook(BaseHook):
    """
    Return Telgram bot hook
    
    :param: token telegram bot token
    """
    def __init__(self, 
                 token: str,   
                 *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.bot: Bot = Bot(token=token)
        
    async def __send_message(self, chat_id, text):
        await self.bot.sendMessage(chat_id=chat_id, text=text, parse_mode="Markdown")
        
    def send_message(self, chat_id, text_messsage: str):
        asyncio.run(self.__send_message(chat_id=chat_id, text=text_messsage))
        
    
        
        