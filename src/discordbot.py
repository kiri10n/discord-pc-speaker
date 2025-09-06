import discord
from discord.ext import commands
from discord import Intents, Client, Interaction
import asyncio

import config

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot起動時に呼び出される関数
@bot.event
async def on_ready():
    print("You started the bot.")

    # スラッシュコマンドを同期
    await bot.tree.sync()

    print("Bot is ready.")

@bot.tree.command()
async def hello_hogehogehoge(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

@bot.tree.command()
async def join(interaction: Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        vc = await channel.connect()
        print(f"Connected to {channel}")
        await interaction.response.send_message("VCに接続しました")
    else:
        print("User is not in a voice channel.")

@bot.tree.command()
async def play(interaction: Interaction):
    vc: discord.VoiceClient = interaction.guild.voice_client
    if not vc:
        print("Bot is not connected to a voice channel.")
        await interaction.response.send_message("まず /join でVCに呼んでください。")
        return

    # VoiceMeeterの仮想デバイスをFFmpegでキャプチャ
    # デバイス名は `ffmpeg -list_devices true -f dshow -i dummy` で確認
    source = discord.FFmpegPCMAudio(
        source="audio=VoiceMeeter Aux Output (VB-Audio VoiceMeeter AUX VAIO)",
        before_options="-f dshow",
        options="-ac 2 -ar 48000"
    )

    vc.play(source)
    print("Started playing audio.")
    await interaction.response.send_message("再生を開始しました。")

@bot.tree.command()
async def stop(interaction: Interaction):
    vc: discord.VoiceClient = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        print("Stopped playing audio.")
        await interaction.response.send_message("停止しました。")

@bot.tree.command()
async def leave(interaction: Interaction):
    vc: discord.VoiceClient = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        print("Disconnected from voice channel.")
        await interaction.response.send_message("切断しました。")

bot.run(config.DISCORD_TOKEN)
