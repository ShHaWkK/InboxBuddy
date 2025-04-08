import discord
from openai import OpenAI
from config import OPENAI_API_KEY
from mails.imap import fetch_latest_mails

client = OpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!mail"):
        query = message.content[5:].strip()

        mails = fetch_latest_mails(3)
        context = "\n".join([f"De: {m['from']}, Sujet: {m['subject']}, Body: {m['body'][:200]}" for m in mails])

        full_prompt = f"Voici des mails :\n{context}\n\nQuestion : {query}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )

        await message.channel.send(response.choices[0].message.content)

# Lancer le bot
bot.run("TON_DISCORD_BOT_TOKEN")
