import traceback
import discord, os
from dotenv import load_dotenv
from discord import app_commands
from post_fetch import PostFetch


load_dotenv()
TOKEN, GUILD_ID = [os.getenv(_) for _ in ["BOT_TOKEN", "GUILD_ID"]]

assert TOKEN, "BOT_TOKEN not found in .env file"
assert GUILD_ID, "GUILD_ID not found in .env file"

GUILD = discord.Object(id=GUILD_ID)


class MyClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        assert self.user, "No client user"
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=GUILD)


client = MyClient()

@client.tree.command(guild=GUILD, description="Start a crosspost")
async def conjure(interaction: discord.Interaction):
    await interaction.response.send_modal(PostFetch())


if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Login failed: {e}")
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
