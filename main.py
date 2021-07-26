# < (c) @xditya >
# This was made for personal use.
# If you are using it, kindly keep credits.

from requests import get
import logging
from telethon import TelegramClient, events
from decouple import config
from datetime import datetime

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

bottoken = None

# start the bot
logging.info("Starting...")
apiid = 6
apihash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

try:
    bottoken = config("BOT_TOKEN")
    auth = [int(x) for x in config("AUTH").split()]
    pincode = config("PIN_CODE")
    age = int(config("AGE"))
except:
    logging.warning("Environment vars are missing! Kindly recheck.")
    logging.info("Bot is quiting...")
    exit()

try:
    bot = (TelegramClient(None, apiid, apihash).start(bot_token=bottoken)).start()
except Exception as e:
    logging.warning(f"ERROR!\n{str(e)}")
    logging.info("Bot is quiting...")
    exit()


logging.info("\n\nStarting to search for Cowin vaccine slots!\n(c) @xditya")


async def processes():  # sourcery no-metrics
    async with bot:
        msg = ""
        for user in auth:
            await bot.send_message(user, "Bot Started.")
        today = datetime.today().strftime("%d-%m-%Y")
        base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(
             pincode, today
        )
        res = get(base_url)
        if res.status_code == 200:
            json = res.json()
            if json["sessions"]:
                for i in json["sessions"]:
                    if (
                        i["min_age_limit"] >= age
                        and i["available_capacity"] > 0
                    ):
                        msg += f"**Centre**: {i['name']}\n"
                        msg += f"**Block**: {i['block_name']}\n"
                        msg += f"**Price**: {i['fee_type']}\n"
                        msg += f"**Availablity**: {i['available_capacity']}\n"
                        if i["vaccine"] != "":
                            msg += f"**Vaccine type**: {i['vaccine']}\n\n"
        if msg != "":
            for user in auth:
                await bot.send_message(user, msg)


bot.loop.run_until_complete(processes())
