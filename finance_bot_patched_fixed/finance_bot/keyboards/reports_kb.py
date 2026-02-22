from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def reports_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Доходы", callback_data="report|income")],
        [InlineKeyboardButton(text="📉 Расходы", callback_data="report|expense")],
        [InlineKeyboardButton(text="⚖️ Сальдо (Доход-Расход)", callback_data="report|balance")],
    ])


def overview_kb_for_type(type_):
    # при первом показе отчёта: сумма, очистка, назад
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сумма всех доходов" if type_ == "income" else "Сумма всех расходов",
                callback_data=f"sum_all|{type_}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🧹 Очистить данные",
                callback_data=f"clear|{type_}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="reports_back"
            )
        ]
    ])


def back_only_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="reports_back")]
    ])
