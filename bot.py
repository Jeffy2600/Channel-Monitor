import discord
from discord.ext import commands
from discord import ui
from discord.ui import View, Button
from discord.utils import get
import logging
import os

logging.basicConfig(level=logging.INFO)

def main():
    # ... รหัสสำหรับเข้าสู่ระบบและทำงานของบอทของคุณ ...

    logging.info("บอทเข้าสู่ระบบเรียบร้อยแล้ว")
    # ... รหัสสำหรับการทำงานอื่นๆ ของบอท ...

    logging.info("บอทออนไลน์แล้ว")

if __name__ == "__bot__":
    main()

# ดึงโทเคนจาก secrets account ของ GitHub
bot_token = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('C!', 'c!'),
    case_insensitive=True,
    intents=intents,
    help_command=None)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} ออนไลน์แล้ว')

@bot.slash_command(name="สร้างหมวดหมู่", description="สร้างหมวดหมู่ใหม่ในเซิร์ฟเวอร์")
async def create_category(ctx, category_name: str):
    existing_category = get(ctx.guild.categories, name=category_name)
    if not existing_category:
        await ctx.guild.create_category(category_name)
        await ctx.respond(f'✅ สร้างหมวดหมู่ "{category_name}" สำเร็จแล้ว.', ephemeral=True)
    else:
        await ctx.respond(f' มีหมวดหมู่ "{category_name}" อยู่แล้ว.', ephemeral=True)

@bot.slash_command(name="สร้างช่อง", description="สร้างช่องใหม่ในเซิร์ฟเวอร์")
async def create_channel(ctx, channel_type: str, category_name: str, *channel_names: str):
    await check_permissions(ctx, "manage_channels")

    category = await create_category(ctx, category_name)

    with async_with(discord.TextChannel(ctx.guild)) as channel:
        await create_channels(channel, channel_type, category_name, channel_names)

async def create_channels(channel: discord.TextChannel, channel_type: str, category_name: str, channel_names: str):
    channel_types = {
        "text": discord.ChannelType.text,
        "voice": discord.ChannelType.voice,
        "forum": discord.ChannelType.forum,
        "announcement": discord.ChannelType.news
    }

    if channel_type not in channel_types:
        await ctx.respond(f" ไม่พบประเภทช่อง: {channel_type}", ephemeral=True)
        return

    for channel_name in channel_names:
        if channel_name.lower() in [channel.name.lower() for channel in ctx.guild.channels]:
            await ctx.respond(f" ชื่อช่อง '{channel_name}' ซ้ำกับช่องที่มีอยู่", ephemeral=True)
            continue

        if channel_type == "text":
            await channel.guild.create_text_channel(channel_name, category=category)
        elif channel_type == "voice":
            await channel.guild.create_voice_channel(channel_name, category=category)
        elif channel_type == "forum":
            await channel.guild.create_stage_channel(channel_name, category=category)
        elif channel_type == "announcement":
            await channel.guild.create_news_channel(channel_name, category=category)

    await ctx.respond(f"✅ สร้างช่อง {channel_type} {', '.join(channel_names)} ภายใต้หมวดหมู่ '{category_name}' สำเร็จแล้วครับ/ค่ะ", ephemeral=True)

async def check_permissions(ctx, permission):
    if not ctx.author.guild_permissions.has_perm(permission):
        await ctx.respond(f"❌ คุณไม่มีสิทธิ์สร้างช่อง", ephemeral=True)
        raise commands.errors.MissingPermissions([permission])

@bot.slash_command(name="ลบหมวดหมู่และช่อง", description="ลบหมวดหมู่และช่องทั้งหมดภายในหมวดหมู่")
async def delete_cac(ctx, category_name: str):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        await ctx.respond(f" ไม่พบหมวดหมู่: {category_name}", ephemeral=True)
        return

    num_channels = len(category.channels)
    await ctx.respond(f"⚠️ ต้องการลบหมวดหมู่ '{category_name}' และช่องทั้งหมด ({num_channels} ช่อง) ใช่หรือไม่? (ตอบกลับด้วย 'ยืนยัน' เพื่อดำเนินการต่อ)", ephemeral=True)

    def check(m):
        return m.author == ctx.author and m.content.lower() == "ยืนยัน"

    try:
        await bot.wait_for_message(check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.respond("❌ ยกเลิกการลบหมวดหมู่", ephemeral=True)
        return

    for channel in category.channels:
        await channel.delete()

    await category.delete()
    await ctx.respond(f"✅ ลบหมวดหมู่ '{category_name}' และช่องทั้งหมด ({num_channels} ช่อง) สำเร็จแล้วครับ/ค่ะ", ephemeral=True)

@bot.slash_command(name="ลบหมวดหมู่", description="ลบหมวดหมู่")
async def delete_category(ctx, category_name: str):
    category = ctx.guild.get_category(name=category_name)
    if not category:
        embed = discord.Embed(title="❌ ไม่พบหมวดหมู่", description=f"ไม่พบหมวดหมู่: {category_name}", color=discord.Color.red())
        await interaction.respond(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(title="⚠️ ต้องการลบหมวดหมู่", description=f"ต้องการลบหมวดหมู่ '{category_name}' ใช่หรือไม่?", color=discord.Color.yellow())
    embed.add_field(name="ยืนยัน", value="กดปุ่ม 'ยืนยัน' เพื่อดำเนินการต่อ", inline=True)

    view = ui.View()

    # เพิ่มปุ่ม "ยืนยัน"
    confirm_button = ui.Button(label="ยืนยัน", style=ui.ButtonStyle.success, custom_id="confirm")
    view.add_item(confirm_button)

    await interaction.respond(embed=embed, view=view)

    response = await view.wait_for(interaction, custom_id="confirm")
    if not response:
        return

    await category.delete()
    embed = discord.Embed(title="✅ ลบหมวดหมู่สำเร็จ", description=f"ลบหมวดหมู่ '{category_name}' เรียบร้อยแล้ว", color=discord.Color.green())
    await interaction.edit_original_response(embed=embed, view=None)


    
@bot.slash_command(name="ลบช่อง", description="ลบช่อง")
async def delete_channel(ctx, *channel_names):
    deleted_channels = []
    for channel_name in channel_names:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            await ctx.respond(f"⚠️ ต้องการลบช่อง '{channel_name}' ใช่หรือไม่? (ตอบกลับด้วย 'ยืนยัน' เพื่อดำเนินการต่อ)", ephemeral=True)

            def check(m):
                return m.author == ctx.author and m.content.lower() == "ยืนยัน"

            try:
                await bot.wait_for_message(check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.respond("❌ ยกเลิกการลบช่อง", ephemeral=True)
                continue

            await channel.delete()
            deleted_channels.append(channel_name)

    if deleted_channels:
        await ctx.respond(f"✅ ลบช่อง {', '.join(deleted_channels)} สำเร็จแล้วครับ/ค่ะ", ephemeral=True)
    else:
        await ctx.respond(" ไม่พบช่องที่ต้องการลบครับ/ค่ะ", ephemeral=True)

@bot.slash_command(name="help", description="แสดงรายการคำสั่งสำหรับการจัดการช่องและหมวดหมู่")
async def help(ctx):
    embed = discord.Embed(title="️ คู่มือบอท ️", description="ใช้คำสั่งเหล่านี้เพื่อจัดการช่องและหมวดหมู่:", color=discord.Color.blue())

    # เพิ่มรายการคำสั่ง
    embed.add_field(name="/สร้างหมวดหมู่", value="สร้างหมวดหมู่ใหม่ในเซิร์ฟเวอร์\nตัวอย่าง: /สร้างหมวดหมู่ เกม", inline=False)
    embed.add_field(name="/สร้างช่อง", value="สร้างช่องใหม่ในเซิร์ฟเวอร์\nตัวอย่าง: /สร้างช่อง text เกมทั่วไป\nตัวอย่าง: /สร้างช่อง voice เกม FPS", inline=False)
    embed.add_field(name="/แก้ไขหมวดหมู่", value="แก้ไขชื่อหมวดหมู่\nตัวอย่าง: /แก้ไขหมวดหมู่ เกม เป็น เกมและการแชท", inline=False)
    embed.add_field(name="/แก้ไขช่อง", value="แก้ไขชื่อช่อง\nตัวอย่าง: /แก้ไขช่อง เกมทั่วไป เป็น เกมสำหรับทุกคน", inline=False)
    embed.add_field(name="/ลบหมวดหมู่และช่อง", value="ลบหมวดหมู่และช่องทั้งหมดภายในหมวดหมู่\nตัวอย่าง: /ลบหมวดหมู่และช่อง เกม", inline=False)
    embed.add_field(name="/ลบหมวดหมู่", value="ลบหมวดหมู่เฉพาะ\nตัวอย่าง: /ลบหมวดหมู่ เกมทั่วไป", inline=False)
    embed.add_field(name="/ลบช่อง", value="ลบช่องเฉพาะ\nตัวอย่าง: /ลบช่อง เกม FPS", inline=False)
    embed.add_field(name="/รายการ", value="แสดงรายชื่อหมวดหมู่และช่องทั้งหมดในเซิร์ฟเวอร์", inline=False)

    await ctx.respond(embed=embed)
    
bot.run(bot_token)
