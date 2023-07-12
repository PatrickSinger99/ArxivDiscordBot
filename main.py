import os
import discord
import dotenv
import scraper
import random
from discord.ext import commands
from discord import app_commands

if __name__ == "__main__":
    # Define intents. Set the data that gets sent to the bot (i think)
    intents = discord.Intents.default()
    intents.message_content = True

    # Define bot
    arxiv_bot = commands.Bot(command_prefix="/", intents=intents)
    coms = ["categories", "recents"]

    # Fetch categories
    scraper.get_categories()

    @arxiv_bot.event
    async def on_ready():
        print(f'Logged on as {arxiv_bot.user}!')

    """
    @arxiv_bot.event
    async def on_message(message):
        # Prevent own message from triggering event and only react to mentions
        if message.author == arxiv_bot.user or arxiv_bot.user not in message.mentions:
            return

        out = "\n".join([arxiv_bot.command_prefix + com for com in coms])
        await message.channel.send(out)
    """

    @arxiv_bot.command()
    async def categories(ctx):
        try:
            cats = scraper.get_categories()
            cats = " :nerd: ".join(["`" + cat + "`" for cat in cats])
            await ctx.send(str(cats))
            return

        except Exception as e:
            print("Failed to get categories. Exception:", e)
            await ctx.send("Gar kein bock")
            return


    @arxiv_bot.command()
    async def recents(ctx, *args):
        arg = " ".join(args)

        try:
            recent_submissions = scraper.get_recent(arg)
            # TEMP TEMP TEMP
            recent_submissions = "\nAuthor usw...\n\n".join(["**" + sub["title"] + "**" for sub in recent_submissions])

            await ctx.send(str(recent_submissions))
            await ctx.message.add_reaction('\N{NERD FACE}')
            return

        except Exception as e:
            print("Failed to get recents. Exception:", e)
            await ctx.send(f"Unknown category \"{arg}\"")
            return


    # Load the environment variables
    dotenv.load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    arxiv_bot.run(token)
