import time
from aiogram import Bot, Router, types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from collections import defaultdict
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import random
import pytz
from config import TOKEN

# Настройки антиспама
MESSAGE_LIMIT = 2  # Лимит сообщений за 1 секунду
TIME_WINDOW = 60  # Время для подсчета нарушений (в секундах)
SPAM_THRESHOLD = 15  # Сколько раз "Please don't spam" за минуту до проверки
BLOCK_THRESHOLD = 20  # Сколько раз "Please don't spam" до блокировки
COOLDOWN_TIMES = [60, 120, 300]  # Время блокировки пользователя (в секундах)

# Храним время последнего сообщения, количество нарушений и блокировки для каждого пользователя
user_last_message_time = defaultdict(lambda: datetime(1970, 1, 1, tzinfo=pytz.UTC))
user_warning_count = defaultdict(int)  # Счетчик предупреждений "Please don't spam"
user_blocked_until = defaultdict(lambda: datetime(1970, 1, 1, tzinfo=pytz.UTC))
user_spam_messages = defaultdict(list)  # Для хранения времени предупреждений "Please don't spam"
user_answers = defaultdict(lambda: None)
user_captcha_active = defaultdict(bool)  # Флаг активности капчи
user_captcha_start_time = defaultdict(datetime)  # Время начала капчи

# Инициализация бота и роутера
bot = Bot(token=TOKEN)
spam_router = Router()

class AntiSpamMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data: dict):
        user_id = event.from_user.id
        current_time = datetime.now(pytz.UTC)

        # Проверяем, заблокирован ли пользователь
        if user_blocked_until[user_id] > current_time:
            time_left = user_blocked_until[user_id] - current_time
            minutes, seconds = divmod(time_left.seconds, 60)
            await event.answer(f"<b>You are blocked for spamming. Try again in {minutes:02}:{seconds:02}.</b>", parse_mode="HTML")
            return

        # Проверяем, активна ли капча
        if user_captcha_active[user_id]:
            # Если капча активна, игнорируем все сообщения
            time_left = 300 - (current_time - user_captcha_start_time[user_id]).seconds  # 5 минут
            if time_left > 0:
                minutes, seconds = divmod(time_left, 60)
                await event.answer(f"<b>Please solve the captcha. You have {minutes:02}:{seconds:02} left.</b>", parse_mode="HTML")
                return
            else:
                # Если время капчи истекло, сбрасываем состояние капчи
                user_captcha_active[user_id] = False

        # Проверяем время между сообщениями
        last_message_time = user_last_message_time[user_id]
        if (current_time - last_message_time).total_seconds() < 0.5:  # Больше 2 сообщений в секунду
            user_warning_count[user_id] += 1

            # Логика для хранения времени каждого предупреждения
            user_spam_messages[user_id].append(current_time)
            # Очищаем список предупреждений старше TIME_WINDOW (60 секунд)
            user_spam_messages[user_id] = [t for t in user_spam_messages[user_id] if current_time - t < timedelta(seconds=TIME_WINDOW)]

            # Если предупреждений "Please don't spam" больше SPAM_THRESHOLD, задаем вопрос
            if len(user_spam_messages[user_id]) >= SPAM_THRESHOLD:
                await self.send_validation_question( event, user_id)
                return

            # Если предупреждений больше BLOCK_THRESHOLD — блокируем пользователя
            if len(user_spam_messages[user_id]) >= BLOCK_THRESHOLD:
                violation_count = len(user_spam_messages[user_id]) - BLOCK_THRESHOLD
                cooldown_time = COOLDOWN_TIMES[min(violation_count, len(COOLDOWN_TIMES) - 1)]
                user_blocked_until[user_id] = current_time + timedelta(seconds=cooldown_time)
                await event.answer(f"<b>Too many spamming attempts! You're blocked for {cooldown_time // 60} minutes.</b>", parse_mode="HTML")
                return

            await event.answer("<b>Please don't spam. Warning.</b>", parse_mode="HTML")
            return

        # Обновляем время последнего сообщения
        user_last_message_time[user_id] = current_time

        # Сбрасываем счетчик предупреждений, если прошло время без спама
        user_warning_count[user_id] = 0

        # Пропускаем сообщение дальше
        return await handler(event, data)
    
    @staticmethod
    async def send_validation_question(event, user_id):
        # Генерируем случайный вопрос
        first_number = random.randint(1, 10)
        second_number = random.randint(1, 10)
        operation = random.choice(["+", "-"])
        question = f"{first_number} {operation} {second_number}"

        # Вычисляем правильный ответ
        correct_answer = first_number + second_number if operation == "+" else first_number - second_number

        # Генерируем варианты ответов
        wrong_answers = [correct_answer + random.randint(1, 3), correct_answer - random.randint(1, 3)]
        options = [correct_answer] + wrong_answers
        random.shuffle(options)

        # Сохраняем правильный ответ для проверки
        user_answers[user_id] = correct_answer

        # Устанавливаем капчу как активную и сохраняем время начала
        user_captcha_active[user_id] = True
        user_captcha_start_time[user_id] = datetime.now(pytz.UTC)

        # Создаем клавиатуру с ответами
        buttons = [InlineKeyboardButton(text=str(option), callback_data=f"answer:{option}") for option in options]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        # Отправляем пользователю вопрос
        await event.answer(f"<b>Are you a bot? Solve this: {question}</b>", reply_markup=keyboard, parse_mode="HTML")


# Обработчик ответа на вопрос
@spam_router.callback_query(lambda c: c.data and c.data.startswith('answer:'))
async def handle_answer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_answer = int(callback_query.data.split(':')[1])
    correct_answer = user_answers.get(user_id)

    if selected_answer == correct_answer:
        await bot.send_message(user_id, "<b>Well done! You're not a bot!</b>", parse_mode="HTML")
        user_warning_count[user_id] = 0  # Сбрасываем предупреждения
        user_spam_messages[user_id] = []  # Очищаем список предупреждений
        user_captcha_active[user_id] = False  # Деактивируем капчу
    else:
        await callback_query.message.reply("<b>Wrong answer. Try again.</b>", parse_mode="HTML")
        # Если ответ неправильный, снова устанавливаем капчу
        await AntiSpamMiddleware.send_validation_question(callback_query.message, user_id)

    # Убираем клавиатуру после ответа
    await callback_query.message.edit_reply_markup(reply_markup=None)

