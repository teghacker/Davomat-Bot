from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup , KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup 
from base import R_Students
import requests
from confik import *
sahifa = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👀 Davomatni Korish", callback_data="korish"), InlineKeyboardButton(text="✏️ Davomat olish", callback_data="olish")],
        [InlineKeyboardButton(text="📝 Yangi Kurs Ochish", callback_data="qoshish")]
    ]
)

help = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kursga O'quvchi Qo'shish", callback_data="qoshish1")],
        [InlineKeyboardButton(text="🚫 Kursdan O'quvchi Ketishi", callback_data="ketish")],
        [InlineKeyboardButton(text="🗑 Kursni yopish", callback_data="yop")],
        [InlineKeyboardButton(text="🗒 Mening Kurslarim", callback_data="Kurs")],
        [InlineKeyboardButton(text="🏘 Bosh menyuga qaytish", callback_data="Bosh")],
    ]
)

boshqa = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️   Ortga", callback_data="Ortga"),InlineKeyboardButton(text="🏘 Bosh menyuga qaytish", callback_data="Bosh")],
    ]
)

ortga = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Bo'ldi", callback_data="boldi")],
    ]
)

hy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ha ✅", callback_data="ha"),InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")],
    ]
)