
import disnake
from disnake.ext import commands
import asyncio
import random
from tabulate import tabulate
import asyncio
import sqlite3
from disnake.ext.commands import Bot, Context, cooldown, has_permissions, BadArgument, MissingPermissions
import os
import requests
import aiohttp
import json
from random import randint
import random
import io
import os
import sqlite3
import datetime
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from tabulate import tabulate
from prettytable import PrettyTable
import random
import spacy
from spacy.lang.en import STOP_WORDS
from disnake.ext import commands
from numpy import array
from disnake import Message




intents = disnake.Intents.all()
bot = commands.Bot(command_prefix = '!', intents=intents)


def get_connection(guild_id, db_name):
    connection = sqlite3.connect(f"{guild_id}_{db_name}.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (name TEXT, inventory TEXT, user_id INTEGER)")
    connection.commit()
    return connection

def add_item(conn, item_name, item_description, item_price):
    cursor = conn.cursor()

    # Проверяем, существует ли уже запись с данным именем предмета
    cursor.execute("SELECT name FROM items WHERE name=?", (item_name,))
    if cursor.fetchone() is not None:
        return False

    # Добавляем новую запись в таблицу items
    cursor.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)", (item_name, item_description, item_price))
    conn.commit()
    return True

def get_connection(guild_id, db_name):
    connection = sqlite3.connect(f"{guild_id}_{db_name}.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (name TEXT, inventory TEXT, user_id INTEGER)")
    connection.commit()
    return connection

def update_user_balance(conn, user_id, change):
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM balances WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO balances (user_id, balance) VALUES (?, ?)", (user_id, change))
    else:
        new_balance = result[0] + change
        cursor.execute("UPDATE balances SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()

def get_user_balance(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM balances WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        return 0
    else:
        return result[0]

# Создаем подключение к SQLite базе данных с разными файлами на каждом сервере
def create_connection(guild_id):
    conn = sqlite3.connect(f"balances_{guild_id}.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS balances (
        user_id TEXT PRIMARY KEY,
        balance INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

# Создаем подключение к SQLite базе данных для магазина
def create_market_connection(guild_id):
    conn = sqlite3.connect(f"market_{guild_id}.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS items (
        name TEXT PRIMARY KEY,
        price INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

def create_inventory_connection(guild_id):
    conn = sqlite3.connect(f"inventory_{guild_id}.db", check_same_thread=False)
    cursor = conn.cursor()

    # Получаем список столбцов таблицы items
    cursor.execute("PRAGMA table_info(items)")
    columns = cursor.fetchall()

    cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
        user_id TEXT PRIMARY KEY,
       inventory balance INTEGER NOT NULL
    )""")
    conn.commit()
    conn.commit()
    return conn

# Команда !р
@bot.command()
async def р(ctx):
    user_id = ctx.author.id
    amount = random.randint(100, 1000)
    
    connection = create_connection(ctx.guild.id)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM balances WHERE user_id=?", (user_id,))
    record = cursor.fetchone()

    if record is None:
        cursor.execute("INSERT INTO balances VALUES (?, ?)", (user_id, amount))
    else:
        cursor.execute("UPDATE balances SET balance=balance+? WHERE user_id=?", (amount, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    await ctx.send(f"{ctx.author.mention}, ваш баланс пополнен на {amount} монет!")

# Команда !б
@bot.command()
async def б(ctx):
    user_id = ctx.author.id

    connection = create_connection(ctx.guild.id)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM balances WHERE user_id=?", (user_id,))
    record = cursor.fetchone()

    if record is None:
        await ctx.send(f"{ctx.author.mention}, вы еще не получили монет. Начните с команды !р!")
    else:
        balance = record[1]
        await ctx.send(f"{ctx.author.mention}, ваш текущий баланс: {balance} монет.")

    cursor.close()
    connection.close()

# Команда !т
@bot.command()
async def работа(ctx):
    user_id = ctx.author.id
    amount = random.randint(1000, 7000)

    connection = create_connection(ctx.guild.id)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM balances WHERE user_id=?", (user_id,))
    record = cursor.fetchone()

    if record is None:
        cursor.execute("INSERT INTO balances VALUES (?, ?)", (user_id, amount))
    else:
        cursor.execute("UPDATE balances SET balance=balance+? WHERE user_id=?", (amount, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    await ctx.send(f"{ctx.author.mention}, вы выиграли {amount} монет!")

# Команда !п
@bot.command()
async def работа1(ctx):
    user_id = ctx.author.id
    amount = random.randint(10, 1500)

    connection = create_connection(ctx.guild.id)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM balances WHERE user_id=?", (user_id,))
    record = cursor.fetchone()

    if record is None:
        cursor.execute("INSERT INTO balances VALUES (?, ?)", (user_id, amount))
    else:
        cursor.execute("UPDATE balances SET balance=balance+? WHERE user_id=?", (amount, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    await ctx.send(f"{ctx.author.mention}, вы получили {amount} монет!")



# Команда !гото для добавления или удаления товаров из магазина
@bot.command()
async def блюдо(ctx, action: str, name: str, price: int):
    if action == "добавить":
        connection = create_market_connection(ctx.guild.id)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (?, ?)", (name, price))
        connection.commit()
        cursor.close()
        connection.close()
        await ctx.send(f"{ctx.author.mention}, товар {name} добавлен в магазин по цене {price} монет!")
    elif action == "удалить":
        connection = create_market_connection(ctx.guild.id)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE name=?", (name,))
        connection.commit()
        cursor.close()
        connection.close()
        await ctx.send(f"{ctx.author.mention}, товар {name} удален из магазина!")
    else:
        await ctx.send(f"{ctx.author.mention}, вы должны добавить или удалить товар из магазина. Используйте !гото добавить/удалить <название товара> <цена товара>")

@bot.command()
async def меню(ctx):
    connection = create_market_connection(ctx.guild.id)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    connection.close()

    if not items:
        await ctx.send("Магазин пока пуст. Используйте !гото, чтобы добавить товары.")
    else:
        embed = disnake.Embed(title="Магазин", color=0x00ff00)
        for item in items:
            name = item[0]
            price = item[1]
            description = "Описание: Lorem ipsum dolor sit amet."

            embed.add_field(name=name, value=f"Цена: {price} монет\n{description}", inline=False)

        await ctx.send(embed=embed)




@bot.command()
async def бай(ctx, name):
    # Получаем подключения к базам данных
    inventory_conn = get_connection(ctx.guild.id, "inventory")
    market_conn = get_connection(ctx.guild.id, "market")
    balance_conn = get_connection(ctx.guild.id, "balance")


    # Получаем информацию о товаре из магазина
    cursor = market_conn.cursor()
    cursor.execute("SELECT price FROM items WHERE name=?", (name,))
    result = cursor.fetchone()

    # Проверяем, удалось ли купить товар
    if result is None:
        await ctx.send(f"Товар '{name}' не найден в магазине")
    elif balance := get_user_balance(balance_conn, ctx.author.id) < result[0]:
        await ctx.send(f"Недостаточно средств для покупки товара '{name}'")
    else:
        # Вычитаем стоимость товара из баланса пользователя
        update_user_balance(balance_conn, ctx.author.id, -result[0])

        # Добавляем товар в инвентарь пользователя
        cursor = inventory_conn.cursor()
        cursor.execute("INSERT INTO items (name, inventory, user_id) VALUES (?, ?, ?)",
                       (name, 1, ctx.author.id))
        inventory_conn.commit()
        await ctx.send(f"Вы купили товар '{name}' за {result[0]} монет")

    # Закрываем подключения к базам данных
    inventory_conn.close()
    market_conn.close()
    balance_conn.close()

@bot.command()
async def ин(ctx):
    # Получаем подключения к базам данных
    inventory_conn = create_inventory_connection(ctx.guild.id)
    balance_conn = create_connection(ctx.guild.id)

    # Получаем информацию об инвентаре пользователя
    cursor = inventory_conn.cursor()
    cursor.execute("SELECT name, inventory FROM items WHERE user_id=?", (ctx.author.id,))
    results = cursor.fetchall()
    items = [f"{name}: {quantity}" for name, quantity in results]

    # Выводим информацию об инвентаре пользователя
    if len(items) == 0:
        await ctx.send("У вас нет товаров в инвентаре")
    else:
        await ctx.send("Ваш инвентарь:\n" + "\n".join(items))

    # Закрываем подключения к базам данных
    inventory_conn.close()

    
    bot.run('token')
