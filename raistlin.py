import traceback
import discord, os
from discord import app_commands
from dotenv import load_dotenv

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


class PostFetch(discord.ui.Modal, title='Post Fetch'):
    postTitle = discord.ui.TextInput(
        label='Title',
        style=discord.TextStyle.short,
        placeholder='Lost Mines of Phandelver',
        required=True,
        max_length=100
    )

    postLocation = discord.ui.TextInput(
        label='Location',
        style=discord.TextStyle.short,
        default="Barley & Sword, North Park, San Diego",
        required=True,
        max_length=100
    )

    postHook = discord.ui.TextInput(
        label='Hook',
        style=discord.TextStyle.short,
        placeholder="A snippet about the game/event to entice folks to join. Goes into the Event and Announcement.",
        required=True,
        max_length=200
    )

    postDescription = discord.ui.TextInput(
        label='Description',
        style=discord.TextStyle.paragraph,
        placeholder="The full description of the game/event. Goes into the forum post.",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Looking forward to {self.postTitle.value}!', ephemeral=False)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=False)

        traceback.print_exception(type(error), error, error.__traceback__)


client = MyClient()


@client.tree.command(guild=GUILD, description="Start a crosspost")
async def conjure(interaction: discord.Interaction):
    await interaction.response.send_modal(PostFetch())


client.run(TOKEN)
