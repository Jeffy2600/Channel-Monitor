import discord
from discord.ext import commands
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

@bot.command()
async def create_category(ctx, *, category_name):
    existing_category = get(ctx.guild.categories, name=category_name)
    if not existing_category:
        await ctx.guild.create_category(category_name)
        await ctx.send(f'✅ สร้างหมวดหมู่ "{category_name}" สำเร็จแล้ว.')
    else:
        await ctx.send(f'🚫 มีหมวดหมู่ "{category_name}" อยู่แล้ว.')

@bot.command()
async def create_channel(ctx, channel_type: str, category_name: str, *channel_names: str):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    new_category_created = False
    if not category:
        category = await ctx.guild.create_category(category_name)
        new_category_created = True

    channel_type = channel_type.lower().strip('"')
    channel_names = [name.strip('"') for name in channel_names]

    channel_types = {
        'text': discord.ChannelType.text,
        'voice': discord.ChannelType.voice,
        'forum': discord.ChannelType.forum,
        'announcement': discord.ChannelType.news
    }

    if channel_type not in channel_types:
        await ctx.send(f"🚫 ไม่พบประเภทช่อง: {channel_type}")
        return

    for channel_name in channel_names:
        if channel_type == 'text':
            await ctx.guild.create_text_channel(channel_name, category=category)
        elif channel_type == 'voice':
            await ctx.guild.create_voice_channel(channel_name, category=category)
        elif channel_type == 'forum':
            await ctx.guild.create_stage_channel(channel_name, category=category)
        elif channel_type == 'announcement':
            await ctx.guild.create_news_channel(channel_name, category=category)

    if new_category_created:
        await ctx.send(f"✅ สร้างหมวดหมู่ '{category_name}' และสร้างช่อง {channel_type} {', '.join(channel_names)} ภายใต้หมวดหมู่นี้สำเร็จแล้วครับ/ค่ะ")
    else:
        await ctx.send(f"✅ สร้างช่อง {channel_type} {', '.join(channel_names)} ภายใต้หมวดหมู่ '{category_name}' สำเร็จแล้วครับ/ค่ะ")

@bot.command()
async def delete_cac(ctx, category_name: str):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        await ctx.send(f"🚫 ไม่พบหมวดหมู่: {category_name}")
        return

    for channel in category.channels:
        await channel.delete()

    await category.delete()
    await ctx.send(f"✅ ลบหมวดหมู่ '{category_name}' และช่องทั้งหมดภายใต้หมวดหมู่นี้สำเร็จแล้วครับ/ค่ะ")

@bot.command()
async def delete_category(ctx, category_name: str):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        await ctx.send(f"🚫 ไม่พบหมวดหมู่: {category_name}")
        return

    await category.delete()
    await ctx.send(f"✅ ลบเฉพาะหมวดหมู่ '{category_name}' สำเร็จแล้วครับ/ค่ะ")

@bot.command()
async def rename_channel(ctx, old_name, *, new_name):
    channel = get(ctx.guild.channels, name=old_name)
    if channel:
        await channel.edit(name=new_name)
        await ctx.send(f'✅ ช่อง "{old_name}" ถูกเปลี่ยนเป็น "{new_name}".')
    else:
        await ctx.send(f'🚫 ไม่พบช่อง "{old_name}".')

@bot.command()
async def delete_channel(ctx, *channel_names):
    deleted_channels = []
    for channel_name in channel_names:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            await channel.delete()
            deleted_channels.append(channel_name)
    if deleted_channels:
        await ctx.send(f"✅ ลบช่อง {', '.join(deleted_channels)} สำเร็จแล้วครับ/ค่ะ")
    else:
        await ctx.send("🚫 ไม่พบช่องที่ต้องการลบครับ/ค่ะ")

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="📚 รายชื่อหมวดหมู่และช่อง 📚", description="🌟 นี่คือรายชื่อของหมวดหมู่และช่องในเซิร์ฟเวอร์:", color=0x1abc9c)
    for category in ctx.guild.categories:
        channels = '\n'.join([f"🔹 {channel.name}" for channel in category.channels])
        embed.add_field(name=f"📂 **{category.name}**", value=channels or "🚫 ไม่มีช่อง", inline=False)
    await ctx.send(embed=embed)

@bot.command()
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

# รันบอท
bot.run(TOKEN)
          
