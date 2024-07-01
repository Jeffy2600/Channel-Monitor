import discord
from discord.ext import commands
import os
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # ... รหัสสำหรับเข้าสู่ระบบและทำงานของบอทของคุณ ...

    logging.info("บอทเข้าสู่ระบบเรียบร้อยแล้ว")
    # ... รหัสสำหรับการทำงานอื่นๆ ของบอท ...

    logging.info("บอทออนไลน์แล้ว")

if __name__ == "__main__":
    main()

bot_token = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

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
