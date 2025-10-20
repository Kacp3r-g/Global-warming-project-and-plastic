import discord
from discord.ext import commands
import random
import os

# ---------- USTAWIENIA ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# ---------- PORADY DOTYCZĄCE ODPADÓW ----------
waste_tips = [
    "Używaj wielorazowych toreb na zakupy zamiast plastikowych.",
    "Kompostuj resztki jedzenia, aby zmniejszyć ilość odpadów.",
    "Unikaj wody butelkowanej — używaj bidonu wielokrotnego użytku.",
    "Kupuj produkty luzem, aby ograniczyć opakowania.",
    "Naprawiaj lub oddawaj rzeczy zamiast je wyrzucać.",
    "Przejdź na elektroniczne paragony i rachunki.",
    "Planuj posiłki, aby nie marnować jedzenia.",
    "Segreguj śmieci zgodnie z lokalnymi zasadami."
]

# ---------- GOTOWE CELE ----------
preset_goals = [
    "Używaj wielorazowych toreb plastikowych zamiast jednorazowych.",
    "Zacznij kompostować resztki jedzenia.",
    "Kupuj środki czystości lub kosmetyki w opakowaniach uzupełnianych."
]

# Proste zapisywanie celów w pamięci
user_goals = {}

# ---------- ZDARZENIA BOTA ----------
@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user}")

    random_tip = random.choice(waste_tips)
    announcement = (
        " **Jestem online i gotowy, aby pomóc Ci ograniczyć ilość odpadów!** ♻️\n"
        f" Dzisiejsza porada: **{random_tip}**\n"
        "Wpisz `$start`, aby dowiedzieć się, jak zacząć!"
    )

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(announcement)
                break

# ---------- KOMENDY ----------
@bot.command()
async def start(ctx):
    """Przywitanie i instrukcja."""
    await ctx.send(
        " **Witaj w Waste Reducer Bot!**\n"
        "Pomogę Ci krok po kroku ograniczyć ilość odpadów w domu.\n"
        "Wpisz `$tip`, aby otrzymać szybką ekoporadę, lub `$addgoal`, aby wybrać swój pierwszy cel!"
    )

@bot.command()
async def tip(ctx):
    """Wysyła losową poradę."""
    tip = random.choice(waste_tips)
    await ctx.send(f" **Dzisiejsza porada:** {tip}")

@bot.command()
async def addgoal(ctx):
    """Pokazuje listę gotowych celów do wyboru."""
    message = " **Wybierz jeden z poniższych celów, aby zacząć redukcję odpadów:**\n"
    for i, goal in enumerate(preset_goals, start=1):
        message += f"{i}. {goal}\n"
    message += "\nWpisz `$choose <numer>`, aby wybrać (np. `$choose 1`)."
    await ctx.send(message)

@bot.command()
async def choose(ctx, number: int):
    """Pozwala użytkownikowi wybrać jeden z celów."""
    user_id = ctx.author.id
    if number < 1 or number > len(preset_goals):
        await ctx.send(" Niepoprawny wybór! Wpisz `$choose 1`, `$choose 2` lub `$choose 3`.")
        return

    chosen_goal = preset_goals[number - 1]
    if user_id not in user_goals:
        user_goals[user_id] = []
    user_goals[user_id].append(chosen_goal)
    await ctx.send(f" Cel dodany: *{chosen_goal}*")

@bot.command()
async def mygoals(ctx):
    """Pokazuje zapisane cele użytkownika."""
    user_id = ctx.author.id
    goals = user_goals.get(user_id, [])
    if not goals:
        await ctx.send("Nie masz jeszcze żadnych celów! Wpisz `$addgoal`, aby dodać pierwszy.")
    else:
        formatted = "\n".join(f"- {g}" for g in goals)
        await ctx.send(f" **Twoje cele związane z ograniczaniem odpadów:**\n{formatted}")

# ---------- URUCHOMIENIE BOTA ----------
bot.run("Token")
