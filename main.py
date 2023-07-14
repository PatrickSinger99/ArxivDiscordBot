import os
import discord
import dotenv
import scraper
import random
from discord.ext import commands

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
        print(f'Logged in as {arxiv_bot.user}')

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
            cats = " | ".join(["`" + cat + "`" for cat in cats])
            await ctx.send(str(cats))
            return

        except Exception as e:
            print("Failed to get categories. Exception:", e)
            await ctx.send("Gar kein bock")
            return


    @arxiv_bot.command()
    async def recents(ctx, *args, num_of_submissions=5,  max_authors=4):
        arg = " ".join(args)

        try:
            recent_submissions = scraper.get_recent(arg, num=num_of_submissions)
            sub_text_blocks = []

            for sub in recent_submissions:
                text_block = ":page_facing_up: **" + sub["title"] + "**\n"
                text_block += " ".join([f"[`{author}`]({sub['author_links'][i]})" for i, author in enumerate(sub["author_names"][:max_authors])])
                if len(sub["author_names"]) > max_authors:
                    text_block += f" + {len(sub['author_names'])-max_authors} more"

                try:
                    text_block += f"\n [Arxiv Link]({sub['paper_link']}) | [PDF Link]({sub['pdf_link']})"
                except:
                    pass

                sub_text_blocks.append(text_block)

            final_text = "\n\n".join(sub_text_blocks)

            # Use embedding message to enable links
            embedded_msg = discord.Embed()
            embedded_msg.description = final_text
            embedded_msg.title = f"Recent Submissions in {arg}"

            await ctx.send(embed=embedded_msg)
            await ctx.message.add_reaction('\N{NERD FACE}')
            return

        except Exception as e:
            print("Failed to get recents. Exception:", e)
            await ctx.send(f"Failed to fetch submissions for category \"{arg}\"")
            return


    # Load the environment variables
    dotenv.load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    arxiv_bot.run(token)
