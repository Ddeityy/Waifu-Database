from config import config
import discord

config()
from db.models import *


class CaptureView(discord.ui.View):
    def __init__(self, attempts: int, waifu: Waifu, user: discord.User):
        super().__init__()
        self.attempts = attempts
        self.waifu = waifu
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user.id

    @discord.ui.button(label=f"Capture", style=discord.ButtonStyle.blurple)
    async def capture_callback(self, button, interaction):
        if self.attempts > 0:
            self.attempts -= 1
            if await roll(self.waifu.rarity):
                await capture_waifu(self.waifu.id, self.user.id)
                button.label = "Success!"
                button.style = discord.ButtonStyle.green
                button.disabled = True
                await interaction.response.edit_message(view=self)
                await interaction.followup.send(
                    f"Captured {format_for_embed(self.waifu.name)}!"
                )
            else:
                button.label = f"Attempts left: {self.attempts}"
                await interaction.response.edit_message(view=self)
        else:
            button.label = "Failed..."
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(
                f"Failed to capture {format_for_embed(self.waifu.name)}.\nGood luck next time!"
            )

    @discord.ui.button(label="Report", style=discord.ButtonStyle.red)
    async def report_callback(self, button, interaction):
        match await report_waifu(self.waifu.id, self.user.id):
            case "SUCCESS":
                button.label = "Reported"
                button.disabled = True
                await interaction.response.edit_message(view=self)
            case "DOUBLE":
                button.label = "Reported"
                button.disabled = True
                await interaction.response.edit_message(view=self)
            case "DENIED":
                button.label = "Reported"
                button.disabled = True
                await interaction.response.edit_message(view=self)

class HaremView(discord.ui.View):
    def __init__(self, waifu, user):
        super().__init__()
        self.waifu = waifu
        self.user = user
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user
    
    @discord.ui.button(label="Release", style=discord.ButtonStyle.red)
    async def release(self, _, interaction):
        user = self.user
        waifu = await get_waifu_by_id(self.waifu)
        name = format_for_embed(waifu.name)
        if waifu.owner_id != None:
            if await release_waifu(waifu.id, user):
                await interaction.response.edit_message(view=None)
                await interaction.followup.send(f"{name} released.")
            else:
                await interaction.response.edit_message(view=None)
                await interaction.followup.send(f"You do not own {name}.")
        else:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(f"{name} has no owner.")


class ResetView(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__()
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user.id

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_callback(self, _, interaction):
        if await reset_user(self.user.id, self.user):
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("User succesfully reset.")
        else:
            await interaction.followup.send("User not found.")

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_callback(self, _, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("User reset aborted.")


async def setup(bot):
    pass
