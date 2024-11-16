import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import callback_query, Message, FSInputFile
from confik import *
from buttons import *
from states import *
from base import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
print('ishladimi')
router = Router()
bot = Bot(token=token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(router)

@router.message(Command('start'))
async def star(message: Message):
    welcome_message = await message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {message.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help
Botdan to'g'ri foydalanish yoriqnomasi /guide""", reply_markup=sahifa)
    await message.delete()


@router.message(Command('help'))
async def star(message: Message):
    welcome_message = await message.answer("🆘 Nima yordam kerak ?", reply_markup=help)
    await message.delete() 


@router.message(Command('guide'))
async def star(message: Message):
    await message.answer('''Quyida bot bilan ishlash yo'riqnomasi:
1) Botning qulayliklardan biri birdan kop kursalrni dovamatini olib borishingiz mumkin
                         
2) Kurs o'quvchilarini kiriting degan oxirgi oquvchini ismini yozgandan so'ng "," vergul qo'ying masalan (Ali Valiyev, Vali Aliyev,) mana shunday     
                                         
3) Va O'quvchilarni Ism va Familiyasini kiritish shart faqat ismini yoki familiyasini kiritsangiz muommaga duch kelishingiz mumkin
                         
4) /help buyrug'ini bossangiz Botning funksiyalaridan foydalanshingiz mumkin masalan guruhga yangi o'quvchi qoshish yokida guruhdan o'quvchi ketishi va hokazalar
                         
5) Qandaydir taklif yokida murojatingiz bolsa <a href="https://t.me/teghacker">admin</a> ga yuzlanishingiz mumkin.''', parse_mode="HTML", disable_web_page_preview=True)
    await message.delete() 

'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'korish')
async def star(call: callback_query, state:FSMContext):
    li=[]
    Kurs=InlineKeyboardBuilder()
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li)>0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Kursni tanlang :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Korish.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")


@router.callback_query(F.data, Korish.start)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    n=0
    if text == 'Ortga':
        welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()
    else:
        for i in R_Davomat():
            if i[3] == text:
                if i[4] == 1 or i[4] == 0:
                    n=1
                    break
        if n==1:
            sana=InlineKeyboardBuilder()
            li=[]
            for i in R_Davomat():
                if i[3] == text:
                    li.append(i[5])
            for i in set(li):
                sana.button(text=f"📅 {i}", callback_data=f'{i}')
            sana.button(text=f"Hammasi", callback_data=f'h')
            sana.button(text=f"Ortga ◀️",callback_data=f"Ortga")
            sana.adjust(2)
            await call.message.answer("Qaysi sanadagi Dovamatni kormoqchisiz :", reply_markup=sana.as_markup())
            await state.update_data({'Course':text})
            await state.set_state(Korish.finish)
            await call.message.delete()
        else:
            await call.answer('Bu guruhdan umuman davomat olinmagan')
            await state.clear()



@router.callback_query(F.data, Korish.finish)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    data = await state.get_data()
    if text == 'Ortga':
        Kurs=InlineKeyboardBuilder()
        username = call.from_user.username
        for i in R_User():
            if i[2] == username:
                Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Kursni tanlang :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Korish.start)
    elif text == 'h':
        result=''
        sana=[]
        for i in R_Davomat():
            if i[3] == data.get("Course"):
                sana.append(i[5])
        for j in set(sana):
            result+=f'Sana: {j}\n'
            for i in R_Davomat():
                if i[3] == data.get("Course"):
                    if i[5] == j:
                        if i[4] == 1:
                            result+=f'{i[2]} - Bor\n'
                        else:
                            result+=f"{i[2]} - Yo'q\n"
            result+='\n\n'
        await call.message.answer(result, reply_markup=boshqa)
        await state.set_state(Korish.boshqa)
        await call.message.delete()
    else:
        result=f'Sana: {text}\n'
        for i in R_Davomat():
            if i[3] == data.get("Course"):
                if f'{i[5]}' == text:
                    if i[4] == 1:
                        result+=f'{i[2]} - Bor\n'
                    else:
                        result+=f"{i[2]} - Yo'q\n"
        await call.message.answer(result, reply_markup=boshqa)
        await state.set_state(Korish.boshqa)
        await call.message.delete()



@router.callback_query(F.data, Korish.boshqa)
async def star(call: callback_query, state:FSMContext):
    text = call.data
    data = await state.get_data()
    if text == 'Ortga':
        sana=InlineKeyboardBuilder()
        li=[]
        for i in R_Davomat():
            if i[3] == data.get("Course"):
                li.append(i[5])
        for i in set(li):
            sana.button(text=f"📅 {i}", callback_data=f'{i}')
        sana.button(text=f"Hammasi", callback_data=f'h')
        sana.button(text=f"Ortga ◀️",callback_data=f"Ortga")
        sana.adjust(2)
        await call.message.answer("Qaysi sanadagi Dovamatni kormoqchisiz :", reply_markup=sana.as_markup())
        await state.set_state(Korish.finish)
        await call.message.delete()
    else:
        welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()



'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'olish')
async def star(call: callback_query, state:FSMContext):
    li=[]
    Kurs=InlineKeyboardBuilder()
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li)>0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Kursni tanlang :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Davomat.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")


@router.callback_query(F.data, Davomat.start)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    n=0
    if text == 'Ortga':
        welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()
    else:
        for i in R_Davomat():
            if i[3] == text:
                if i[5] == f'{datetime.date(datetime.now())}':
                    n=1
                    break
        if n==0:
            d=[]
            for i in R_Students():
                if i[2] == text:
                    d.append(i[1])
            for i in d:
                ismlar = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text=f"bor {i}", callback_data=f"{i} bor"), InlineKeyboardButton(text=f"yoq {i}", callback_data=f"{i} yoq")]
                    ]
                )
                await call.message.answer(f"{i} o'quvchi bor yoki yoq",reply_markup=ismlar)
            await call.message.answer(f"Davomat olib bo'lingandan keyin pastdagi tugmani bosing",reply_markup=ortga)
            await state.update_data({'Course':text})
            await state.set_state(Davomat.finish)
            await call.message.delete()
        else:
            await call.answer('Bu guruhdan allaqochan bugungi davomat olingan')
            await state.set_state(Davomat.start)


@router.callback_query(F.data, Davomat.finish)
async def star(call: callback_query,state:FSMContext):
    text=(f'{call.data[:-4]}')
    data = await state.get_data()
    guruh = data.get("Course")
    royhat = []
    if call.data == 'boldi':
        await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.message.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()
        await call.message.delete()
    else:
        for i in R_Students():
            if i[1] == text:
                if call.data[-1] == 'r':
                    add_to_dovamat(i[0],text,data.get("Course"),1)
                    break
                else:add_to_dovamat(i[0],text,data.get("Course"))
        await state.set_state(Davomat.finish)
        await call.message.delete()


'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'ketish')
async def star(call: callback_query, state:FSMContext):
    Kurs=InlineKeyboardBuilder()
    li=[]
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li) !=0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Qaysi Kursdan :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Ketish.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")


@router.callback_query(F.data, Ketish.start)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'Ortga':
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    else:
        Kurs=InlineKeyboardBuilder()
        for i in R_Students():
            if i[2] == text:
                Kurs.button(text=f"🎓 {i[1]}",callback_data=f"{i[1]}")
        # Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Qaysi o'quvchini :", reply_markup=Kurs.as_markup())
        await state.update_data({'Course':text})
        await state.set_state(Ketish.yangi)
        await call.message.delete()


@router.callback_query(F.data, Ketish.yangi)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    await call.message.answer("Ishonchingiz kamilmi 👌", reply_markup=hy)
    await state.update_data({'oquvchi':text})
    await state.set_state(Ketish.finish)
    await call.message.delete()


@router.callback_query(F.data, Ketish.finish)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'ha':
        data = await state.get_data()
        id=0
        for i in R_Students():
            if i[1] == data.get("oquvchi"):
                id=i[0]
                break
        for i in R_Davomat():
            if i[1] == id:
                Delete_Davomat(id)
        Delete_Student(id)
        await call.answer(f'Ish muvaffaqiyotli yakunlandi ✅')
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    else:
        await call.answer(f'Ish bekor qilindi ❌')
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()

'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'yop')
async def star(call: callback_query, state:FSMContext):
    Kurs=InlineKeyboardBuilder()
    li=[]
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li) !=0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Qaysi Kursni Yopmoqchisiz :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Yopish.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")


@router.callback_query(F.data, Yopish.start)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'Ortga':
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    else:
        await call.message.answer("Ishonchingiz kamilmi 👌", reply_markup=hy)
        await state.update_data({'Course':text})
        await state.set_state(Yopish.finish)
        await call.message.delete()


@router.callback_query(F.data, Yopish.finish)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'ha':
        data = await state.get_data()
        id=0
        for i in R_User():
            if i[3] == data.get("Course"):
                id=i[0]
                break
        for i in R_Students():
            if i[2] == data.get("Course"):
                Delete_Student(i[0])
                Delete_Davomat(i[0])
        Delete_User(id)
        await call.answer(f'Ish muvaffaqiyotli yakunlandi ✅')
        await call.message.answer("Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    else:
        await call.answer(f'Ish bekor qilindi ❌')
        await call.message.answer("Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()

'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'qoshish1')
async def star(call: callback_query, state:FSMContext):
    Kurs=InlineKeyboardBuilder()
    li=[]
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li) !=0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga") 
        Kurs.adjust(2)
        await call.message.answer("Qaysi Kursga qo'shmoqchisiz :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Yangi.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")


@router.callback_query(F.data, Yangi.start)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'Ortga':
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    else:
        await state.update_data({'Course':text})
        await call.message.answer(f"""O'quvchilarni quyidagicha yuboring Ali,Vali,...,Sali,""")
        await call.message.delete()
        await state.set_state(Yangi.finish)


@router.message(F.text, Yangi.finish)
async def S(m: Message, state: FSMContext):
    data = await state.get_data()
    s=''
    li=[]
    for i in [m.text]:
        for j in i:
            if j==",":
                li.append(s)
                s=''
            else:s+=j
    for i in li:
        ADD_Students(i,data.get("Course"))
    await m.answer(f'Ish muvaffaqiyotli yakunlandi ✅')
    await m.answer("🆘Nima yordam kerak", reply_markup=help)
    await m.delete()
    await state.clear()
    
'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'qoshish')
async def star(call: callback_query, state:FSMContext):
    await call.message.answer(f"""Kurs nomini yozib yuboring""")
    await call.message.delete()
    await state.set_state(Kurs_q.start)


@router.message(F.text, Kurs_q.start)
async def S(m: Message, state: FSMContext):
    course = m.text
    username = m.from_user.username 
    user_id = m.from_user.id
    await state.update_data({'Course':course})
    ADD_User(user_id,username,course)
    await m.answer("Kurs muvvafaqiyatli yaratildi")
    await m.answer("""O'quvchilarni quyidagicha yuboring Ali,Vali,...,Sali,""")
    await m.delete()
    await state.set_state(Kurs_q.finish)

@router.message(F.text, Kurs_q.finish)
async def S(m: Message, state: FSMContext):
    data = await state.get_data()
    s=''
    li=[]
    for i in [m.text]:
        for j in i:
            if j=="'":continue
            elif j==",":
                li.append(s)
                s=''
            else:s+=j
    for i in li:
        ADD_Students(i,data.get("Course"))
    await m.answer(f'{data.get("Course")} kursga o\'quvchilar muvaffaqiyotli qo\'shildi ✅')
    await m.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {m.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
    await m.delete()
    await state.clear()

'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'Kurs')
async def star(call: callback_query, state:FSMContext):
    Kurs=InlineKeyboardBuilder()
    li=[]
    username = call.from_user.username
    for i in R_User():
        if i[2] == username:
            Kurs.button(text=f"📝 {i[3]}",callback_data=f"{i[3]}")
            li.append(i[3])
    if len(li) !=0:
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga")
        Kurs.button(text=f"🏘 Bosh menyuga qaytish",callback_data=f"Bosh")
        Kurs.adjust(2)
        await call.message.answer("Sizning Kurslaringiz :", reply_markup=Kurs.as_markup())
        await call.message.delete()
        await state.set_state(Kurs1.start)
    else:await call.answer("Sizda hali umuman Kurs yoq")



@router.callback_query(F.data, Kurs1.start)
async def star(call: callback_query, state:FSMContext):
    text = call.data
    if text == 'Ortga':
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    elif text == "Bosh":
        welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()
    else:
        Kurs=InlineKeyboardBuilder()
        for i in R_Students():
            if i[2] == text:
                Kurs.button(text=f"🎓 {i[1]}",callback_data=f"{i[1]}")
        Kurs.button(text=f"Ortga ◀️",callback_data=f"Ortga")
        Kurs.button(text=f"🏘 Bosh menyuga qaytish",callback_data=f"Bosh")
        Kurs.adjust(2)
        await call.message.answer("Kurs O'quvchilari :", reply_markup=Kurs.as_markup())
        await state.set_state(Kurs1.finish)
        await call.message.delete()


@router.callback_query(F.data, Kurs1.finish)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text == 'Ortga':
        await call.message.answer("🆘 Nima yordam kerak", reply_markup=help)
        await call.message.delete()
        await state.clear()
    elif text == "Bosh":
        welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
        await call.message.delete()
        await state.clear()

'------------------------------------------------------------------------------------------------------------------------------'

@router.callback_query(F.data == 'Ortga')
async def star(call: callback_query):
    welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
    await call.message.delete()

@router.callback_query(F.data == 'Bosh')
async def star(call: callback_query):
    welcome_message = await call.message.answer_photo(photo='https://blog.polleverywhere.com/hubfs/Comms%20l%20Blog%20l%20Images/hands-in-air.png', caption=f"""Assalom alaykum {call.from_user.full_name}
Dovamat botga xush kelibsiz !
Yordam kerak bo'lsa /help""", reply_markup=sahifa)
    await call.message.delete()


@router.message(F.text)
async def star(message: Message):
    await message.answer("🆘 Nima yordam kerak", reply_markup=help)
    await message.delete()

'------------------------------------------------------------------------------------------------------------------------------'


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())