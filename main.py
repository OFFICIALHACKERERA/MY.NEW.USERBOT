import asyncio
import random
import os
import time
from datetime import timedelta
from platform import python_version
from telethon import TelegramClient, events, functions, Button, version
from telethon.sessions import StringSession
from telethon.errors import ChatAdminRequiredError, UserNotParticipantError

# Replace these with your actual config details
APP_ID = int(os.environ.get("APP_ID", 22030138))
API_HASH = os.environ.get("API_HASH", "c6c02e51a03f6b03dba9ad9a826dc2f1")

# Define string sessions
LEGEND_STRINGS = [
    os.environ.get("LEGEND_STRING_1", "your_string_1"),
    os.environ.get("LEGEND_STRING_2", "your_string_2")
]

BOT_USERNAME = os.environ.get("BOT_USERNAME", "@YourBotUsername")
ALLOWED_USER_ID = 6508157803  # Replace with your actual user ID
mention = "@raoxc"
legendversion = "1.0"
StartTime = time.time()

# Create a list of Telegram clients for each session
legends = [
    TelegramClient(StringSession(session), api_id=APP_ID, api_hash=API_HASH, auto_reconnect=True)
    for session in LEGEND_STRINGS
]

IPIC = "https://telegra.ph/file/6bb3994d5789d8e7f2c99.mp4"
RAID = ["hello ", "hii "]
active_raids = {}

def get_readable_time(seconds):
    return str(timedelta(seconds=seconds))

async def is_user_allowed(event):
    return event.sender_id == ALLOWED_USER_ID

async def handle_alive_command(event):
    if not await is_user_allowed(event):
        return

    uptime = get_readable_time(time.time() - StartTime)
    emoji = random.choice(["✥", "✔️", "⭐", "✨", "☣️", "🔰", "🏴", "‍☠️" ,"🚀"])
    my = random.choice(["🇦🇱", "💠", "🔷", "🔹"])

    legend_caption = (
    f"**─────────────────**\n"
    f"**DYOH USERBOT IS ONLINE {my}**\n"
    f"**─────────────────**\n"
    f"**╭───────────────**\n"
    f"**┣{emoji} Telethon version :** `{version.__version__}`\n"
    f"**┣{emoji} Userbot Version :** `{legendversion}`\n"
    f"**┣{emoji} Python Version :** `{python_version()}`\n"
    f"**┣{emoji} Uptime :** {uptime}\n"
    f"**┣{emoji} Master:** {mention}\n"
    f"╰─────────────────\n")

    buttons = [[Button.url("Repo", "https://github.com/ITS-LEGENDBOT/LEGENDBOT")]]

    await event.client.send_file(
        event.chat_id,
        IPIC,
        caption=legend_caption,
        buttons=buttons
    )

async def register_handlers(legend):
    @legend.on(events.NewMessage(pattern="alive$"))
    async def alive_handler(event):
        await handle_alive_command(event)

    @legend.on(events.NewMessage(pattern=r"spam (\d+) (.+)"))
    async def spammer(event):
        if not await is_user_allowed(event):
            return

        try:
            count = int(event.pattern_match.group(1))
            text = event.pattern_match.group(2)
        except (ValueError, IndexError):
            return await event.reply("Usage: spam <count> <text>")

        sleep_time = 1 if count > 50 else 0.5
        await event.delete()  # Delete the original command message
        for _ in range(count):
            await event.respond(text)
            await asyncio.sleep(sleep_time)

    @legend.on(events.NewMessage(pattern=r"raid (\d+)"))
    async def raid(event):
        if not await is_user_allowed(event):
            return

        if not event.reply_to_msg_id:
            return await event.reply("Please reply to a user's message to start the raid.")

        reply_msg = await event.get_reply_message()
        try:
            count = int(event.pattern_match.group(1))
        except ValueError:
            return await event.reply("Usage: raid <count> (reply to a user)")

        user = await event.client.get_entity(reply_msg.sender_id)
        username = f"[{user.first_name}](tg://user?id={user.id})"

        for _ in range(count):
            await event.client.send_message(event.chat_id, f"{username} {random.choice(RAID)}")
            await asyncio.sleep(0.3)

    @legend.on(events.NewMessage(pattern=r"replyraid$"))
    async def add_reply_raid(event):
        if not await is_user_allowed(event):
            return

        if event.reply_to_msg_id is None:
            return await event.reply("Reply to a User's message to activate raid on them.")

        reply_msg = await event.get_reply_message()
        user = await event.client.get_entity(reply_msg.sender_id)

        if not user:
            return await event.reply("Could not retrieve user information.")

        if event.chat_id not in active_raids:
            active_raids[event.chat_id] = []

        if user.id in active_raids[event.chat_id]:
            return await event.reply("The user is already enabled with Raid.")

        active_raids[event.chat_id].append(user.id)
        await event.reply(f"Raid Has Been Started for {user.first_name}.")

    @legend.on(events.NewMessage(pattern=r"dreplyraid$"))
    async def remove_chatbot(event):
        if not await is_user_allowed(event):
            return

        if event.reply_to_msg_id is None:
            return await event.reply("Reply to a User's message to stop the raid on them.")

        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = event.chat_id

        if chat_id in active_raids and user_id in active_raids[chat_id]:
            active_raids[chat_id].remove(user_id)
            if not active_raids[chat_id]:
                del active_raids[chat_id]
            await event.reply("Raid has been stopped for the user.")
        else:
            await event.reply("The user is not activated with raid.")

    @legend.on(events.NewMessage(pattern=r"j ([\s\S]+)"))
    async def join_channel(event):
        channel_username = event.pattern_match.group(1).strip()
        joining_message = await event.reply("Joining...")

        try:
            channel = await legend.get_entity(channel_username)
            participant = await legend(functions.channels.GetParticipantRequest(channel, 'me'))
            await joining_message.delete()
            await event.reply("Error: The bot is already a member of this channel.")
        except UserNotParticipantError:
            try:
                await legend(functions.channels.JoinChannelRequest(channel_username))
                await joining_message.delete()
                await event.reply("Joined successfully.")
            except ChatAdminRequiredError:
                await joining_message.delete()
                await event.reply("Error: The bot needs to be an admin to join this channel.")
            except Exception as e:
                await joining_message.delete()
                await event.reply(f"An error occurred: {str(e)}")
        except Exception as e:
            await joining_message.delete()
            await event.reply(f"An error occurred: {str(e)}")

    @legend.on(events.NewMessage(pattern=r"e ([\s\S]+)"))
    async def exit_channel(event):
        channel_username = event.pattern_match.group(1).strip()
        leaving_message = await event.reply("Leaving...")

        try:
            channel = await event.get_entity(channel_username)
            await legend(functions.channels.LeaveChannelRequest(channel))
            await leaving_message.delete()
            await event.reply("Left the channel successfully.")
        except Exception as e:
            await leaving_message.delete()
            await event.reply(f"An error occurred: {str(e)}")

    @legend.on(events.NewMessage(incoming=True))
    async def ai_reply(event):
        if event.chat_id in active_raids and event.sender_id in active_raids[event.chat_id]:
            await event.reply(random.choice(RAID))

# Main execution
async def main():
    await asyncio.gather(*[register_handlers(legend) for legend in legends])
    await asyncio.gather(*[legend.start() for legend in legends])
    await asyncio.gather(*[legend.run_until_disconnected() for legend in legends])

# Colab mein run karne ke liye
if __name__ == "__main__":
    asyncio.run(main())
