# post_fetch.py
import discord, traceback


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
    
    postContentDefault = """Supplies are needed in the frontier town of Phandalin! Will you help?

Then replace me (as well as much space as you need)"""

    postContent = discord.ui.TextInput(
        label='Hook & Description',
        style=discord.TextStyle.paragraph,
        default=postContentDefault,
        required=True,
        max_length=200
    )
    
    postTimes = discord.ui.TextInput(
		label='When will it be?',
		style=discord.TextStyle.short,
		default="12/31/25 6:00 PM - 9:00 PM",
        required=True,
		max_length=100
	)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Looking forward to {self.postTitle.value}!', ephemeral=False)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=False)

        traceback.print_exception(type(error), error, error.__traceback__)
