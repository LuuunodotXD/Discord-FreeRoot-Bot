import discord
from discord.ext import commands
import os
import asyncio
import datetime
from dotenv import load_dotenv

load_dotenv()

class MeuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.start_time = datetime.datetime.utcnow()

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"  ✅ Cog carregado: {filename[:-3]}")

        synced = await self.tree.sync()
        print(f"  🔄 {len(synced)} slash commands sincronizados!")

    async def on_ready(self):
        atividade = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servidor(es) | /ajuda"
        )
        await self.change_presence(status=discord.Status.online, activity=atividade)
        print(f"\n🤖 Bot online: {self.user} (ID: {self.user.id})")
        print(f"📡 Conectado em {len(self.guilds)} servidor(es)\n")

bot = MeuBot()
bot.run(os.getenv("DISCORD_TOKEN"))
