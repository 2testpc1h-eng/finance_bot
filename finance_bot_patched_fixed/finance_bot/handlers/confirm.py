from finance_bot.utils import display_date
from finance_bot import database_helpers as dbh


async def send_save_confirmation(message, op_type, category, amount, date_obj):
    user_id = message.from_user.id

    # получаем общий итог (включая только что добавленную запись)
    total_sum = dbh.sum_by_type_and_category(
        user_id=user_id,
        type_=op_type,
        category=category,
        period=None
    )

    # предыдущая сумма до добавления записи
    try:
        previous_sum = total_sum - float(amount)
    except Exception:
        previous_sum = total_sum

    date_str = display_date(date_obj)

    reply = (
        "✅ Запись сохранена\n"
        f"📅 {date_str}\n"
        f"💰 {previous_sum:.2f} + {float(amount):.2f}\n\n"
        f"Итого: {total_sum:.2f}р"
    )

    await message.answer(reply)
