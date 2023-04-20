from base.module import command, callback_query, BaseModule
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import httpx
import time
import datetime

class UASiren(BaseModule):
    @command("uasiren")
    async def uasiren(self, _, message: Message):
        """Show alarm list """
        async with httpx.AsyncClient() as http_client:
            startsiren = self.S["siren"]["launch"]
            btn = self.S["siren"]["button"]
            last_update = self.S["siren"]["lastupd"]
            response = await http_client.get("https://alarmmap.online/assets/json/_alarms/siren.json")
            siren = response.json()

        string = ""
        for item in siren:
            start_time = datetime.datetime.fromisoformat(item['start'][:-6]) + datetime.timedelta(hours=3)
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            string += f"🛑 <b>{item['district']}</b>\n       {startsiren} <code>{start_time_str}</code>\n"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=btn,
                        callback_data="update_list"
                    )
                ]
            ]
        )
        last_update_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        message_text = f"{string}\n{last_update} {last_update_time}"
        await message.reply_text(message_text, reply_markup=keyboard)

    @callback_query(filters.regex("update_list"))
    async def update_list(self, _, callback_query):
        message = callback_query.message
        await callback_query.answer()
        async with httpx.AsyncClient() as http_client:
            startsiren = self.S["siren"]["launch"]
            last_update = self.S["siren"]["lastupd"]
            response = await http_client.get("https://alarmmap.online/assets/json/_alarms/siren.json")
            siren = response.json()

        string = ""
        for item in siren:
            start_time = datetime.datetime.fromisoformat(item['start'][:-6]) + datetime.timedelta(hours=3)
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            string += f"🛑 <b>{item['district']}</b>\n       {startsiren} <code>{start_time_str}</code>\n"


        last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message_text = f"{string}\n{last_update}{last_update_time}"
        await message.edit_text(message_text, reply_markup=message.reply_markup)
