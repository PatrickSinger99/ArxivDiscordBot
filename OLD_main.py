import os
import discord
import dotenv
import scraper
import random
from discord.ext import commands


class ArxivBot(commands.Bot):
    def __init__(self, **kwargs):
        kwargs.setdefault('command_prefix', '/')
        # Set the data that gets sent to the bot (i think)
        kwargs.setdefault('intents', discord.Intents.default())
        kwargs['intents'].message_content = True

        super().__init__(**kwargs)

        # Fetch categories
        scraper.get_categories()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        # Prevent own message from triggering event and only react to mentions
        if message.author == self.user or self.user not in message.mentions:
            return

        print(f'Message from {message.author}: {message.content}')

        # Clean message: Remove bot mention and leading/trailing whitespaces
        prompt = message.content.replace(self.user.mention, "").strip().lower()

        # CASE: Send Categories
        if prompt in ["categories", "category", "cat", "cats"]:
            try:
                categories = scraper.get_categories()
                categories = "\n".join([cat for cat in categories])


                await message.channel.send(str(categories))
                return
            except Exception as e:
                print(e)
                await message.channel.send("Gar kein bock")
                return

        # CASE: Get recents
        if "test" in prompt:
            selected_category = prompt.replace("test", "").strip()
            try:
                recents = scraper.get_recent(selected_category)

                await message.channel.send(str(recents)[:2000])
                return

            except Exception as e:
                print(e)
                await message.channel.send(f"Unknown category \"{selected_category}\"")
                return

        await message.channel.send(random.choice(["was", "The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start."]))



if __name__ == "__main__":
    # Load the environment variables
    dotenv.load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    bot = ArxivBot()
    bot.run(token)
