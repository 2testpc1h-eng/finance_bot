from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from finance_bot.handlers.record import INCOME_CATS, EXPENSE_CATS

# Главное меню отчётов
reports_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 По датам", callback_data="report_dates"),
            InlineKeyboardButton(text="📊 График по категории", callback_data="report_chart_cat")
        ]
    ]
)

# Меню выбора категории для графика
def categories_kb():
    buttons = []
    for cat in list(INCOME_CATS) + list(EXPENSE_CATS):
        buttons.append(
            [InlineKeyboardButton(text=cat, callback_data=f"cat_chart|{cat}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
