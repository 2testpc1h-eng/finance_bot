# finance_bot v16
1)Удали старое виртуальное окружение
В папке проекта:

rmdir /s /q venv

2) Создай новое venv уже на Python 3.11
Убедись, что версия правильная:

python --version


3) Создай новое venv уже на Python 3.11
Убедись, что версия правильная:

python --version


4)Должно быть:
Python 3.11.x

5) Установи зависимости 

python -m venv venv
venv\Scripts\activate
pip install -U aiogram
pip install aiogram==2.25.1 python-dotenv matplotlib pandas

6) Запусти бота
venv\Scripts\activate
python -m finance_bot.bot

Итоговый набор зависимостей (под твой проект)
Запомни или сохрани:
pip install aiogram==3.4.1 python-dotenv matplotlib pandas

Если хочешь, можешь создать requirements.txt:

aiogram==3.4.1
python-dotenv
matplotlib
pandas
