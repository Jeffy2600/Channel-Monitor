import discord
from discord.ext import commands
import os

bot_token = os.environ['BOT_TOKEN']

# สร้าง Client
bot = commands.Bot(command_prefix='!')

# ฟังก์ชั่นยกเลิกคำสั่ง Slash Command ทั้งหมด
@bot.event
async def on_ready():
  # ดึงรายการคำสั่ง Slash Command ทั้งหมด
  commands = await bot.application.commands.fetch()

  # ลบคำสั่ง Slash Command ทีละรายการ
  for command in commands:
    await command.delete()

  # แจ้งเตือนว่าลบคำสั่ง Slash Command ทั้งหมดเรียบร้อย
  print("ลบคำสั่ง Slash Command ทั้งหมดเรียบร้อย")

# เริ่มรันบอท
bot.run('bot_token')
