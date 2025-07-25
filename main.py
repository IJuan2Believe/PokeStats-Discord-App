import discord 
import requests
base_url = "https://pokeapi.co/api/v2"
from discord import app_commands 
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
import os 


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

 
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"We are ready to go, {bot.user.name}")


@bot.hybrid_command(name="dex", description="Display Pokédex entry for a Pokémon")
async def dex(ctx, pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
        sprite = data["sprites"]["front_default"]
        height = data["height"] / 10   
        weight = data["weight"] / 10   

      
        species_url = f"{base_url}/pokemon-species/{pokemon_name.lower()}"
        species_response = requests.get(species_url)

        if species_response.status_code == 200:
            species_data = species_response.json()
            flavor_text = next(
                (entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
                 for entry in species_data["flavor_text_entries"]
                 if entry["language"]["name"] == "en"),
                "No Dex-entry available."
            )
        else:
            flavor_text = "Could not retrieve Pokédex entry."

        if species_response.status_code == 200:
            species_data = species_response.json()
        genus_name = next(
            (entry["genus"] for entry in species_data["genera"]
             if entry["language"]["name"] == "en"),
            "No genus available."
        )

        embed = discord.Embed(title=f"{name} Info", color=0xFF0000)
        embed.add_field(name="Species", value=f"The {genus_name}", inline=True)
        embed.add_field(name="Type", value=types, inline=False)
        embed.add_field(name="Height", value=f"{height} m", inline=True)
        embed.add_field(name="Weight", value=f"{weight} kg", inline=True)
        embed.add_field(name="Dex-entry", value=flavor_text, inline=False)
 
        embed.set_thumbnail(url=sprite)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Pokémon '{pokemon_name}' not found.")



 
@bot.hybrid_command(name="stats", description="Display base stats for a Pokémon")
async def stats(ctx,pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
  
    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
        sprite = data["sprites"]["front_default"]

        #pokemon stats 
        hp = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "hp"), None)
        attack = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "attack"), None)
        defense = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "defense"), None)
        special_attack = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "special-attack"), None)
        special_defense = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "special-defense"), None)
        speed = next((stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "speed"), None)
 
        
        # there is probably a better way to do this but I am not sure how to do it yet
        hp_color = "⚪"
        if hp <= 30:
            hp_color = "🔴"
        elif hp <= 59:
            hp_color = "🟠"
        elif hp <= 89:
            hp_color = "🟡" 
        elif hp <= 110:
            hp_color = "🟢"
        else:
            hp_color = "🔵"   
        
        attack_color = "⚪"
        if attack <= 30:
            attack_color = "🔴"
        elif attack <= 59:
            attack_color = "🟠"
        elif attack <= 89:
            attack_color = "🟡" 
        elif attack <= 110:
            attack_color = "🟢"
        else:
            attack_color = "🔵"   

        defense_color = "⚪"
        if defense <= 30:
            defense_color = "🔴"
        elif defense <= 59:
            defense_color = "🟠"
        elif defense <= 89:
            defense_color = "🟡" 
        elif defense <= 110:
            defense_color = "🟢"
        else:
            defense_color = "🔵"   
        
        special_attack_color = "⚪"
        if special_attack <= 30:
            special_attack_color = "🔴"
        elif special_attack <= 59:
            special_attack_color = "🟠"
        elif special_attack <= 89:
            special_attack_color = "🟡" 
        elif special_attack <= 110:
            special_attack_color = "🟢"
        else:
            special_attack_color = "🔵"   

        special_defense_color = "⚪"
        if special_defense <= 30:
            special_defense_color = "🔴"
        elif special_defense <= 59:
            special_defense_color = "🟠"
        elif special_defense <= 89:
            special_defense_color = "🟡" 
        elif special_defense <= 110:
            special_defense_color = "🟢"
        else:
            special_defense_color = "🔵"   
        
        speed_color = "⚪"
        if speed <= 30:
            speed_color = "🔴"
        elif speed <= 59:
            speed_color = "🟠"
        elif speed <= 89:
            speed_color = "🟡" 
        elif speed <= 110:
            speed_color = "🟢"
        else:
            speed_color = "🔵"   
        
            
 
           
        stats_list = (
        f"{hp_color}HP: {hp}\n"
        f"{attack_color}Attack: {attack}\n"
        f"{defense_color}Defense: {defense}\n"
        f"{special_attack_color}Special Attack: {special_attack}\n"
        f"{special_defense_color}Special Defense: {special_defense}\n"
        f"{speed_color}Speed: {speed}"
        )
 
        embed = discord.Embed(title=f"{name} Info", color=0xFFD700)
        embed.add_field(name="Type", value=types, inline=False)
        embed.add_field(name="Stats",value=stats_list, inline=False)
        embed.set_thumbnail(url=sprite)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Pokémon '{pokemon_name}' not found ")



         
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
