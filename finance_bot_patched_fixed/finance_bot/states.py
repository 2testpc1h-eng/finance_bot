from aiogram.fsm.state import StatesGroup, State

class RecordStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_subcategory = State()
    waiting_for_amount = State()

class ReportStates(StatesGroup):
    waiting_for_start = State()
    waiting_for_end = State()
    waiting_for_cat = State()
