from aiogram.fsm.state import State, StatesGroup


class Kurs_q(StatesGroup):
    start = State()
    finish = State()

class Kurs1(StatesGroup):
    start = State()
    finish = State()

class Yangi(StatesGroup):
    start = State()
    finish = State()

class Yopish(StatesGroup):
    start = State()
    finish = State()

class Ketish(StatesGroup):
    start = State()
    yangi = State()
    finish = State()

class Davomat(StatesGroup):
    start = State()
    finish = State()

class Korish(StatesGroup):
    start = State()
    finish = State()
    boshqa = State()

