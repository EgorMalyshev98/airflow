import datetime
from airflow.notifications.basenotifier import BaseNotifier
from hooks.telegram_hook import TelegramBotHook
from telegram import Bot
import pendulum


class TelegramNotification(BaseNotifier):
    
    def __init__(self, 
                 telegram_bot_token=None,
                 telegram_chat_id=None):
        
        self.telegram_bot_token=telegram_bot_token
        self.telegram_chat_id=telegram_chat_id
        super().__init__()


    def notify(self, context):
        
        tg_hook = TelegramBotHook(token=self.telegram_bot_token)

        task_id = context["ti"].task_id
        task_state = context["ti"].state
        dag_name = context["ti"].dag_id
        start_date = context["ti"].start_date + datetime.timedelta(hours=3)
        end_date = context["ti"].end_date + datetime.timedelta(hours=3)

        message_template = (f"Dag name: `{dag_name}` \n"
                            f"Task id: `{task_id}` \n"
                            f"Task State: `🔴{task_state}🔴` \n"
                            f"Start date: `{start_date}` \n"
                            f"End date: `{end_date}` \n"
                            )

        tg_hook.send_message(chat_id=self.telegram_chat_id,
                             text_messsage=message_template)