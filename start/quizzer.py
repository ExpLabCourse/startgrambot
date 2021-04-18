from typing import List
import logging
import config
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot)

class Quiz:
    type: str = "quiz"

    quizzes_database = {}
    quizzes_owners = {}

    def __init__(self, quiz_id, question, options, correct_option_id, owner_id):
        self.quiz_id: str = quiz_id
        self.question: str = question
        self.options: List[str] = [*options]
        self.correct_option_id: int = correct_option_id
        self.owner: int = owner_id
        self.winners: List[int] = []
        self.chat_id: int = 0
        self.message_id: int = 0

    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        poll_keyboard.add(types.KeyboardButton(text="Создать викторину",
                                               request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
        poll_keyboard.add(types.KeyboardButton(text="Отмена"))
        await message.answer("Нажмите на кнопку ниже и создайте викторину!", reply_markup=poll_keyboard)

    @dp.message_handler(lambda message: message.text == "Отмена")
    async def action_cancel(message: types.Message):
        remove_keyboard = types.ReplyKeyboardRemove()
        await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)

    @dp.message_handler(content_types=["poll"])
    async def msg_with_poll(message: types.Message):

        if not quizzes_database.get(str(message.from_user.id)):
            quizzes_database[str(message.from_user.id)] = []


        if message.poll.type != "quiz":
            await message.reply("Извините, я принимаю только викторины (quiz)!")
            return

        quizzes_database[str(message.from_user.id)].append(Quiz(
            quiz_id=message.poll.id,
            question=message.poll.question,
            options=[o.text for o in message.poll.options],
            correct_option_id=message.poll.correct_option_id,
            owner_id=message.from_user.id)
        )

        quizzes_owners[message.poll.id] = str(message.from_user.id)

        await message.reply(
            f"Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}")

        @dp.inline_handler() 
        async def inline_query(query: types.InlineQuery):
            results = []
            user_quizzes = quizzes_database.get(str(query.from_user.id))
            if user_quizzes:
                for quiz in user_quizzes:
                    keyboard = types.InlineKeyboardMarkup()
                    start_quiz_button = types.InlineKeyboardButton(
                        text="Отправить в группу",
                        url=await deep_linking.get_startgroup_link(quiz.quiz_id)
                    )
                    keyboard.add(start_quiz_button)
                    results.append(types.InlineQueryResultArticle(
                        id=quiz.quiz_id,
                        title=quiz.question,
                        input_message_content=types.InputTextMessageContent(
                            message_text="Нажмите кнопку ниже, чтобы отправить викторину в группу."),
                        reply_markup=keyboard
                    ))
            await query.answer(switch_pm_text="Создать викторину", switch_pm_parameter="_",
                               results=results, cache_time=120, is_personal=True)


    if __name__ == "__main__":
        executor.start_polling(dp, skip_updates=True)