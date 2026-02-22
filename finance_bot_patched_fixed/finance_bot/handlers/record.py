from finance_bot import database_helpers as dbh
from datetime import date
from aiogram import Router, F
from .confirm import send_save_confirmation
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from finance_bot.states import RecordStates


router = Router()

INCOME_CATS = {
    "Зарплата": ["Наличные", "Карта"]
}


EXPENSE_CATS = {
    "Еда": [],
    "Жилье": [],
    "Развлечения": [],
    "Здоровье": [],
    "Подарки": [],
    "Транспорт": ["Такси", "Общественный транспорт"]
}


def make_inline_cats(type_str, user_id=None):
    kb = []
    parent = {"income": INCOME_CATS, "expense": EXPENSE_CATS}
    default_map = parent.get(type_str, {})
    defaults = list(default_map.keys())
    user_cats = []
    if user_id is not None:
        try:
            user_cats = dbh.get_categories(user_id, type_str) or []
        except Exception:
            user_cats = []
    cats = defaults + [c for c in user_cats if c not in defaults]
    for c in cats:
        kb.append([InlineKeyboardButton(text=c, callback_data=f"rec_cat|{c}")])
    # Add row with add and delete category buttons using unified callback format
    kb.append([
        InlineKeyboardButton(text='➕ Добавить категорию', callback_data=f"rec_addcat|{type_str}"),
        InlineKeyboardButton(text='➖ Удалить категорию', callback_data=f"rec_delcat_init|{type_str}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def make_inline_subs(cat):
    kb = []
    parent = {**INCOME_CATS, **EXPENSE_CATS}
    for s in parent.get(cat, []):
        kb.append([InlineKeyboardButton(text=s, callback_data=f"rec_sub|{s}")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "➕ Доход")
async def inc_start(msg: Message, state: FSMContext):
    await state.clear()
    await state.update_data(type="income")
    await msg.answer("Выберите категорию:", reply_markup=make_inline_cats("income", msg.from_user.id))
    await state.set_state(RecordStates.waiting_for_category)


@router.message(F.text == "➖ Расход")
async def exp_start(msg: Message, state: FSMContext):
    await state.clear()
    await state.update_data(type="expense")
    await msg.answer("Выберите категорию:", reply_markup=make_inline_cats("expense", msg.from_user.id))
    await state.set_state(RecordStates.waiting_for_category)


@router.callback_query(F.data.startswith("rec_cat|"))
async def cat_chosen(call: CallbackQuery, state: FSMContext):
    cat = call.data.split("|")[1]
    await state.update_data(category=cat)
    await call.message.delete()

    parent = {**INCOME_CATS, **EXPENSE_CATS}
    if parent.get(cat):
        await call.message.answer(
            "Выберите подкатегорию:",
            reply_markup=make_inline_subs(cat)
        )
        await state.set_state(RecordStates.waiting_for_subcategory)
    else:
        await call.message.answer("Введите сумму:")
        await state.set_state(RecordStates.waiting_for_amount)


@router.callback_query(F.data.startswith("rec_sub|"))
async def sub_chosen(call: CallbackQuery, state: FSMContext):
    sub = call.data.split("|")[1]
    await state.update_data(subcategory=sub)
    await call.message.delete()

    await call.message.answer("Введите сумму:")
    await state.set_state(RecordStates.waiting_for_amount)


@router.message(RecordStates.waiting_for_amount)
async def amount(msg: Message, state: FSMContext):
    try:
        amt = float(msg.text.replace(",", "."))
    except ValueError:
        await msg.answer("Введите число, например: 1500")
        return

    data = await state.get_data()
    user_id = msg.from_user.id
    today = date.today()

    # сохраняем запись (ШАГ 5)
    dbh.add_operation(
        user_id,
        data["type"],
        data["category"],
        data.get("subcategory"),
        amt,
        today.isoformat()
    )

    # подтверждение
    await send_save_confirmation(
        msg,
        data["type"],
        data["category"],
        amt,
        today
    )

    await state.clear()

# === dynamic category helpers ===

def add_category(cat_type, name):
    if cat_type=='income':
        INCOME_CATS.setdefault(name, [])
    else:
        EXPENSE_CATS.setdefault(name, [])

def delete_category(cat_type, name):
    if cat_type=='income':
        INCOME_CATS.pop(name, None)
    else:
        EXPENSE_CATS.pop(name, None)
