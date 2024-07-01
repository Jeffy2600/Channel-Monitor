import discord
from discord import ui
from discord.ui import View, Button
from discord.utils import get
import logging
import os

logging.basicConfig(level=logging.INFO)

def main():
    # ดึงโทเคนจาก secrets account ของ GitHub
    bot_token = os.environ['BOT_TOKEN']

    # สร้าง intents ของบอท
    intents = discord.Intents.default()
    intents.message_content = True

    # สร้าง Bot
    bot = commands.Bot(
        intents=intents,
        help_command=None
    )

    # class สำหรับคำสั่ง Slash Command
    class MyCommands(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        # คำสั่ง Slash Command "สร้างหมวดหมู่"
        @bot.command(name="สร้างหมวดหมู่")
        async def create_category(self, ctx: Interaction, category_name: str):
            # ตรวจสอบสิทธิ์ผู้ใช้
            if not ctx.author.guild_permissions.manage_channels:
                await ctx.respond("ขออภัย คุณไม่มีสิทธิ์สร้างหมวดหมู่")
                return

            # สร้างช่องใหม่ (ประเภทหมวดหมู่)
            new_category = await ctx.guild.create_category(name=category_name)
            await ctx.respond(f"สร้างหมวดหมู่ '{category_name}' เรียบร้อยแล้ว")

    # เพิ่ม Cog เข้ากับ Bot
    bot.add_cog(MyCommands(bot))

    # รอให้ Bot พร้อมใช้งาน
    @bot.event
    async def on_ready():
        print(f'✅ {bot.user.name} ออนไลน์แล้ว')
        await bot.application.commands.sync(guild_ids=[YOUR_GUILD_ID])

    # รัน Bot
    bot.run(bot_token)

if __name__ == "__main__":
    main()

