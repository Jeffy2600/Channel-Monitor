import discord
from discord.ext import commands
from discord.ui import View, Button
from discord.utils import get
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # ... รหัสสำหรับเข้าสู่ระบบและทำงานของบอทของคุณ ...

    logging.info("บอทเข้าสู่ระบบเรียบร้อยแล้ว")
    # ... รหัสสำหรับการทำงานอื่นๆ ของบอท ...

    logging.info("บอทออนไลน์แล้ว")

if __name__ == "__main__":
    main()

# โหลดโทเค็นจากไฟล์ .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        await ctx.respond(f" ไม่พบหมวดหมู่: {category_name}", ephemeral=True)
        return

    await ctx.respond(f"⚠️ ต้องการลบหมวดหมู่ '{category_name}' ใช่หรือไม่? (ตอบกลับด้วย 'ยืนยัน' เพื่อดำเนินการต่อ)", ephemeral=True)

    def check(m):
        return m.author == ctx.author and m.content.lower() == "ยืนยัน"

    try:
        await bot.wait_for_message(check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.respond("❌ ยกเลิกการลบหมวดหมู่", ephemeral=True)
        return

    await category.delete()
    await ctx.respond(f"✅ ลบหมวดหมู่ '{category_name}' สำเร็จแล้วครับ/ค่ะ", ephemeral=True)

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

@bot.slash_command(name="รายการ", description="แสดงรายชื่อหมวดหมู่และช่อง")
async def list(ctx):
    embed = discord.Embed(title=" รายชื่อหมวดหมู่และช่อง ", description=" นี่คือรายชื่อของหมวดหมู่และช่องในเซิร์ฟเวอร์:", color=0x1abc9c)

    num_categories = len(ctx.guild.categories)
    num_channels = sum(len(category.channels) for category in ctx.guild.categories)
    embed.add_field(name=" สรุป", value=f"หมวดหมู่: {num_categories} | ช่อง: {num_channels}", inline=False)

    for category in sorted(ctx.guild.categories, key=lambda c: c.name):
        channels = sorted([f" {channel.name}" for channel in category.channels], key=lambda c: c.lower())
        embed.add_field(name=f" **{category.name}**", value='\n'.join(channels) or " ไม่มีช่อง", inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(name="รายการคำสั่ง", description="แสดงรายการคำสั่งสำหรับจัดการช่องและหมวดหมู่")
async def help(ctx):
    embed = discord.Embed(
        title="🛠️ คู่มือบอท 🛠️",
        description="ใช้คำสั่งเหล่านี้เพื่อจัดการช่องและหมวดหมู่:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="📚 ดูรายชื่อหมวดหมู่และชื่อช่องภายใต้หมวดหมู่นั้นๆ",
        value="พิมพ์: `c!list`",
        inline=False
    )
    embed.add_field(
        name="📁 สร้างหมวดหมู่",
        value="พิมพ์: `c!create_category \"ชื่อหมวดหมู่\"`\nตัวอย่าง: `c!create_category \"เกมส์\"`",
        inline=False
    )
    embed.add_field(
        name="💬 สร้างช่อง(สามารถสร้างหมวดหมู่ใหม่พร้อมกับช่องได้)",
        value="พิมพ์: `c!create_channel \"ประเภทช่อง\" \"ชื่อหมวดหมู่\" \"ชื่อช่อง1\" \"ชื่อช่อง2\" ...`\nประเภทช่องที่มี: `\"ช่องข้อความ คือ text\" \"ช่องเสียง คือ voice\" \"ช่องฟอรั่ม คือ forum\" \"ช่องประกาศ คือ news\"  \"ช่องเวที(ลำดับขั้น) คือ stage\"`\nตัวอย่าง: `c!create_channel \"text\" \"เกมส์\" \"พูดคุย\" \"แชทเรื่องเกม\"`",
        inline=False
    )
    embed.add_field(
        name="✏️ เปลี่ยนชื่อช่อง",
        value="พิมพ์: `c!rename_channel \"ชื่อเดิม\" \"ชื่อใหม่\"`\nตัวอย่าง: `c!rename_channel \"พูดคุย\" \"แชทหลัก\"`",
        inline=False
)
    embed.add_field(
        name="🗑️ ลบหมวดหมู่",
        value="พิมพ์: `c!delete_category \"ชื่อหมวดหมู่\"`\nตัวอย่าง: `c!delete_category \"แชทหลัก\"`",
        inline=False
)
    embed.add_field(
        name="🗑️ ลบหมวดหมู่และช่องทั้งหมดที่อยู่ภายใต้หมวดหมู่นั้น",
        value="พิมพ์: `c!delete_cac \"ชื่อหมวดหมู่\"`\nตัวอย่าง: `c!delete_cac \"แชทหลัก\"`",
        inline=False
    )
    embed.add_field(
        name="🗑️ ลบช่อง(ลบได้ตั้งแต่ 1 ช่องขึ้นไป)",
        value="พิมพ์: `c!delete_channel \"ชื่อช่อง1\" \"ชื่อช่อง2\" ...`\nตัวอย่าง: `c!delete_channel \"แชทหลัก\" \"เกมส์\" \"แชทเกมส์\"`",
        inline=False
    )
    embed.set_footer(text="💡 โปรดใส่ชื่อที่มีเว้นวรรคภายในเครื่องหมายคำพูด (\") เพื่อการทำงานที่ถูกต้อง")

    await ctx.send(embed=embed)

async def list_help_embed(interaction):
    embed = discord.Embed(title=" รายการคำสั่ง", description="ใช้คำสั่งเหล่านี้เพื่อดูรายการหมวดหมู่และช่อง", color=discord.Color.blue())
    embed.add_field(name="/รายการ", value="แสดงรายชื่อหมวดหมู่และช่องทั้งหมดในเซิร์ฟเวอร์", inline=False)
    await interaction.edit_message(embed=embed)

# รันบอท
bot.run(TOKEN)
          
