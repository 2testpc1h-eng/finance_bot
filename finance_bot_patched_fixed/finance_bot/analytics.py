import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

def get_df():
    from finance_bot import database as _database
    conn = _database.conn
    df = pd.read_sql("SELECT * FROM operations", conn)
    # привести date к datetime, если возможно
    try:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    except Exception:
        pass
    return df

def _plot_grouped_by_month_and_category(df: pd.DataFrame, out_path: str):
    """
    Построить сгруппированный столбчатый график: по оси X -- месяц (YYYY-MM),
    для каждого месяца -- столбцы для категорий (сумма amount по категории за месяц).
    """
    if df.empty:
        raise ValueError("Empty dataframe for plotting")

    # Убедимся, что date -- datetime
    if not pd.api.types.is_datetime64_any_dtype(df.get("date")):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date"])
    # Представление месяца в формате YYYY-MM (строка) для удобной подписи
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # сводная таблица: index=month, columns=category, values=amount (sum)
    pivot = df.pivot_table(index="month", columns="category", values="amount", aggfunc="sum", fill_value=0)

    # сортировка месяцев по хронологии (index сейчас строки YYYY-MM)
    try:
        pivot.index = pd.to_datetime(pivot.index.astype(str), format="%Y-%m")
        pivot = pivot.sort_index()
        # для отображения подписи вернём индекс обратно в строковый формат YYYY-MM
        pivot.index = pivot.index.to_series().dt.strftime("%Y-%m")
    except Exception:
        # если не удалось парсить, оставляем как есть
        pivot = pivot.sort_index()

    # ограничение числа категорий — топ-8 + Other
    if pivot.shape[1] > 8:
        totals = pivot.sum(axis=0).sort_values(ascending=False)
        top_categories = totals.head(8).index.tolist()
        other = pivot.drop(columns=top_categories).sum(axis=1)
        pivot = pivot[top_categories].copy()
        pivot["Other"] = other

    # Если слишком много месяцев, можно показать только последние 24 (2 года). 
    # Здесь оставляем все, но можно изменить при желании.
    ax = pivot.plot(kind="bar", figsize=(12, 6))
    ax.set_xlabel("Месяц (YYYY-MM)")
    ax.set_ylabel("Сумма")
    ax.set_title("Распределение по категориям по месяцам")
    # Легенда снизу
    ax.legend(title="Категория", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.clf()

async def report_dates(msg, start, end):
    """
    Строит и отправляет сгруппированный график по категориям за период start..end,
    где столбцы — по МЕСЯЦАМ (интервал = 1 месяц).
    """
    df = get_df()
    # фильтруем по датам — пробуем конвертировать
    try:
        start_ts = pd.to_datetime(start)
        end_ts = pd.to_datetime(end)
        df = df[(df.date >= start_ts) & (df.date <= end_ts)]
    except Exception:
        # fallback на строковую фильтрацию (если даты в БД не в datetime)
        df = df[(df.date >= start) & (df.date <= end)]

    if df.empty:
        await msg.answer("Нет данных в этот период")
        return

    out = "chart_period.png"
    try:
        _plot_grouped_by_month_and_category(df, out)
    except Exception as e:
        await msg.answer(f"Ошибка при построении графика: {e}")
        return

    with open(out, "rb") as fh:
        await msg.answer_photo(photo=fh)

async def report_chart(msg, cat):
    """
    Построить график для конкретной категории по МЕСЯЦАМ (интервал 1 месяц).
    """
    df = get_df()
    df = df[df.category == cat]

    if df.empty:
        await msg.answer(f"Нет данных по {cat}")
        return

    # привести к datetime и сгруппировать по month
    if not pd.api.types.is_datetime64_any_dtype(df.get("date")):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    series = df.groupby("month")["amount"].sum().sort_index()

    # Попытаемся упорядочить месяцы хронологически, если строки формата YYYY-MM
    try:
        series.index = pd.to_datetime(series.index, format="%Y-%m")
        series = series.sort_index()
        series.index = series.index.to_series().dt.strftime("%Y-%m")
    except Exception:
        pass

    ax = series.plot(kind="bar", figsize=(10,4))
    ax.set_xlabel("Месяц (YYYY-MM)")
    ax.set_ylabel("Сумма")
    ax.set_title(f"{cat} по месяцам")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out = "chart_cat.png"
    plt.savefig(out)
    plt.clf()

    with open(out, "rb") as fh:
        await msg.answer_photo(photo=fh)
