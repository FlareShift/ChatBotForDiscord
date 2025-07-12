import os
import discord
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

client_openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_message = message.content.strip()
    if not user_message:
        return

    prompt = (
        "Ты дружище с района, отвечаешь просто и по-пацански, "
        "используешь лёгкий сленг, но при этом остаёшься вежливым и помогаешь по делу.\n\n"
        + user_message
    )

    try:
        response = client_openai.chat.completions.create(
            model="google/gemma-3n-e2b-it:free",
            messages=[
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "MyDiscordBot"
            }
        )
        reply = response.choices[0].message.content
        await message.channel.send(reply)
    except Exception as e:
        await message.channel.send(f"❌ Ошибка API: {e}")

client.run(DISCORD_TOKEN)
