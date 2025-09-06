import os
from discord import Intents, Client, Interaction
from discord.app_commands import CommandTree
from dotenv import load_dotenv
load_dotenv()

import config


class MyClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)


async def setup_hook(self) -> None:

    await self.tree.sync()


    async def on_ready(self):
        print(f"login: {self.user.name} [{self.user.id}]")


intents = Intents.default()
client = MyClient(intents=intents)


@client.tree.command()
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')


client.run(config.DISCORD_TOKEN)

