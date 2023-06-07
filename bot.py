import os
import asyncio
import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv

from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.models import models as db


logger = logging.getLogger(__name__)
config = load_dotenv()

messages = [
    "Первая статья предназначена для абсолютных"
    "новичков в ООП на Python и содержит основы"
    "объектно-ориентированного программирования на языке Python."
    "Вторая статья описывает концепции, принципы и примеры реализации ООП на Python."
    "Третья статья содержит общую информацию об ООП и" 
    "может быть полезна для более глубокого"
    "понимания темы.\n\n"
    "1. https://proglib.io/p/vvedenie-v-obektno-orientirovannoe-programmirovanie-oop-na-python-2020-07-23 \n"
    "2. https://proglib.io/p/python-oop \n"
    "3. https://habr.com/ru/hub/oop/ \n",

    "Первая статья предназначена для начинающих и содержит основы программирования компьютеров с помощью Python. \n"
    "Вторая статья содержит список бесплатных ресурсов для изучения Python на русском и английском языках. \n"
    "Третья статья - это бесплатный онлайн курс по Python (питон) для начинающих от CodeBasics. \n\n"
    "1. https://www.coursera.org/learn/python-ru"
    "2. https://proglib.io/p/top-20-besplatnyh-resursov-dlya-izucheniya-python-sohrani-eto-v-zakladki-2021-01-08"
    "3. https://code-basics.com/ru/languages/python",
    
    "Несколько крайне полезных ссылок для начинающих питонистов. \n\n"
    "1. https://proglib.io/p/bystryy-samouchitel-kak-osvoit-python-za-30-minut-2021-01-11 \n"
    "2. https://skillbox.ru/media/code/kak-izuchit-python-samostoyatelno-i-besplatno/ \n"
    "3. https://ru.bitdegree.org/rukovodstvo/python-samouchitel/ \n"
    "4. https://python-scripts.com/learn-python \n",

    "Интересная статья с множеством полезного для Pyhton-Dev:\n"
    "https://pythonworld.ru/samouchitel-python",

    "Официальная документация Python - великолепный источник мудрости," 
    "непосредственно от создателей Python! Здесь вы найдете полное руководство по языку,"
    "библиотекам и модулям. Поражающее разнообразие информации, достойное похвалы!\n"
    "Ссылка: [Документация Python](https://docs.python.org/3/)\n\n",

    "Real Python - высококлассный ресурс с большим количеством статей, руководств "
    "и видеокурсов для изучения Python. Их материалы снабжены образцами кода и пошаговыми инструкциями. "
    "Чистый бриллиант!\n"
    "Ссылка: [Real Python](https://realpython.com/)\n\n",
    
    "Python.org - святилище Python с увлекательными новостями, руководствами и множеством "
    "ресурсов для участия в сообществе. Если вы ищете свежие новости и важные анонсы, "
    "вам стоит заглянуть сюда. Незаменимый инструмент в битве с неведением!\n"
    "Ссылка: [Python.org](https://www.python.org/)\n\n"
    
    "Stack Overflow - легендарный форум программистов, где вы можете задавать вопросы "
    "и находить ответы на все ваши проблемы. Множество разработчиков, готовых помочь, "
    "и огромный архив вопросов и ответов. Здесь ни один вопрос не останется без внимания!\n"
    "Ссылка: [Stack Overflow](https://stackoverflow.com/)\n\n",
    
    "Python Weekly - еженедельная подборка новостей, статей, руководств и событий Python. "
    "Быть в курсе последних трендов и событий в мире Python - легкое задание "
    "с помощью этого письма. Как музыка в радиоактивном мире!\n"
    "Ссылка: [Python Weekly](https://www.pythonweekly.com/)\n\n"
    
    "Hitchhiker's Guide to Python - путеводитель по Python, который поможет вам "
    "освоиться в путанице пакетов, проектов и инструментов. Здесь вы найдете советы и рекомендации "
    "для эффективного и качественного программирования. Как верный гид в бескрайних пустошах Python!\n"
    "Ссылка: [Hitchhiker's Guide to Python](https://docs.python-guide.org/)\n\n",
    
    "Страница Python на ресурсе Toster - место, где можно задавать вопросы и находить ответы "
    "по различным аспектам Python. Здесь собрана обширная база знаний и опытных разработчиков. "
    "Ощутите истинный вкус знаний на этой странице!\n"
    "Ссылка: [Python на Toster](https://toster.ru/tag/python)\n\n",
    
    "Хабр - популярный IT-ресурс с множеством статей и обсуждений по разным темам, "
    "включая Python. Здесь вы найдете полезные материалы, руководства и советы от профессионалов. "
    "Изобилие знаний, которое ожидает вас на страницах Хабра!\n"
    "Ссылка: [Хабр](https://habr.com/ru/hub/python/)\n\n",
    
    "Pythonworld - русскоязычный портал о Python, где собраны статьи, руководства и справочники "
    "по разным аспектам языка. Здесь вы найдете информацию о базовых и продвинутых темах Python. "
    "Присоединяйтесь к путешествию в мир Python на странице Pythonworld!\n"
    "Ссылка: [Pythonworld](https://pythonworld.ru/)\n\n"
    
    "Proglib - ресурс с большим количеством статей и уроков по программированию на Python. "
    "Здесь вы найдете обзоры библиотек, примеры кода и интересные решения. Один шаг - и вы в мире Proglib!\n"
    "Ссылка: [Proglib](https://proglib.io/p/python)\n\n",
    
    "Python-scripts - сайт, где собраны примеры и скрипты на Python для различных задач. "
    "Здесь вы найдете исходный код и описания к примерам, которые помогут вам разобраться в разных аспектах Python. "
    "Узнайте больше на странице Python-scripts!\n"
    "Ссылка: [Python-scripts](https://python-scripts.com/)\n\n"
    
    "Хороший программист - блог с полезными статьями и уроками по Python. Здесь вы найдете "
    "информацию о языке, библиотеках и советы по разработке. Прокачайте свои навыки на странице Хорошего программиста!\n"
    "Ссылка: [Хороший программист](https://goodprogrammer.ru/tag/python)\n\n",
    
    "Pythonist - портал с уроками и статьями для изучения Python. Здесь вы найдете материалы "
    "по основам, продвинутым темам и различным областям применения Python. Погрузитесь в мир Python на странице Pythonist!\n"
    "Ссылка: [Pythonist](https://pythonist.ru/)\n\n",
    
    "WebDev - ресурс, посвященный веб-разработке, включая Python и его фреймворки. Здесь вы найдете "
    "статьи, уроки и советы по разработке веб-приложений на Python. Раскройте свой потенциал на странице WebDev!\n"
    "Ссылка: [WebDev](https://webdevblog.ru/tag/python/)\n\n"
    
    "Pythonworld - блог с полезными статьями и руководствами для программистов на Python. Здесь вы найдете "
    "информацию о языке, библиотеках, фреймворках и практические примеры. Расширьте свои горизонты на странице Pythonworld!\n"
    "Ссылка: [Pythonworld](https://pythonworld.ru/)\n\n",
    
    "Python-club - русскоязычный портал для программистов на Python. Здесь вы найдете статьи, "
    "уроки, новости и интересные материалы по различным аспектам языка. Присоединяйтесь к Python-клубу!\n"
    "Ссылка: [Python-club](https://python-club.ru/)\n\n",


    "Официальная документация FastAPI - оригинальный источник знаний о фреймворке FastAPI, "
    "разработанный автором самого FastAPI, Себастьяном Рамирезом. Здесь вы найдете полное руководство, "
    "документацию по функциям, моделям и схемам, а также множество примеров. Ваш надежный путеводитель в мире FastAPI!\n"
    "Ссылка: [Документация FastAPI](https://fastapi.tiangolo.com/ru/)\n\n",
    
    "FastAPI - модернизированный фреймворк для создания веб-приложений на Python. В этой статье вы узнаете, "
    "что такое FastAPI и как он отличается от других фреймворков. Готовьтесь к великолепной разработке с FastAPI!\n"
    "Ссылка: [FastAPI](https://ru.wikipedia.org/wiki/FastAPI)\n\n",

    "Roadmap.sh - Roadmap.sh предоставляет обширную коллекцию roadmap'ов для различных областей разработки, включая веб-разработку, "
    "мобильную разработку, машинное обучение, кибербезопасность и многое другое. Выберите нужную область и следуйте пошаговым инструкциям, "
    "чтобы достичь своих целей.\n"
    "Ссылка: [Roadmap.sh](https://roadmap.sh/)\n\n",
    
    
    "DevRoadmap - DevRoadmap предоставляет подробные roadmap'ы для различных языков программирования, фреймворков, "
    "библиотек и других технологий. Здесь вы найдете детальные пути обучения и рекомендации по развитию навыков в выбранных областях.\n"
    "Ссылка: [DevRoadmap](https://devroadmap.io/)\n\n",
    
    
    "CodePath - CodePath предлагает roadmap'ы для студентов и начинающих разработчиков по различным областям разработки, "
    "включая мобильную разработку, веб-разработку, кибербезопасность и тестирование программного обеспечения. "
    "Изучайте и развивайтесь с CodePath!\n"
    "Ссылка: [CodePath](https://codepath.org/)\n\n",
    
    
    "Fullstack Roadmap - Fullstack Roadmap представляет roadmap для развития навыков полноценного разработчика. "
    "Здесь вы найдете пути обучения и рекомендации по изучению фронтенда, бэкенда, баз данных и других ключевых технологий. "
    "Идите к полному стеку с Fullstack Roadmap!\n"
    "Ссылка: [Fullstack Roadmap](https://github.com/kamranahmedse/developer-roadmap)\n\n"
    
    
    "Open Source Society University - Open Source Society University предлагает roadmap'ы для самообучения в различных областях "
    "разработки и компьютерных наук. Здесь вы найдете пути для изучения таких тем, как алгоритмы, операционные системы, "
    "сети, базы данных и многое другое. Станьте студентом Open Source Society University!\n"
    "Ссылка: [Open Source Society University](https://github.com/ossu/computer-science)\n\n",

]


async def start():
    db.sql_start()
    logger.info("Бот запущен")
    logger.info("Создание таблиц в базе данных выполнено")


selected_messages = []


async def send_posts(bot):
    print("отправка постов!")
    while True:
        try:
            print(len(messages))
            # Проверяем, все ли сообщения были уже выбраны
            if len(selected_messages) == len(messages):

                # Если все сообщения были выбраны, сбрасываем список выбранных сообщений
                await bot.send_message(-1001929746261, "Ожидайте следующих постов!")


            # Выбираем случайный элемент из списка, исключая уже выбранные сообщения
            message = random.choice(list(set(messages) - set(selected_messages)))

            # Добавляем выбранное сообщение в список выбранных сообщений
            selected_messages.append(message)
            await asyncio.sleep(86400)

            await bot.send_message(-1001929746261, message)
        except Exception as e:
            logger.error(e)


async def send_polly(bot):
    # Создание объекта голосования
    msg = (
        "🌟 Программисты, собираемся ли мы на оффлайн-встречу? 🌟\n\n"
        "💻 Электронные устройства и онлайн-связь – наша повседневность.\n"
        "Но может быть, пора оторваться от кода "
        "и встретиться в реальном мире? 🌍\n\n"
        "пошутить о наших любимых багах. 🤣\n"
        "❓ Поддерживаете ли вы идею оффлайн-встречи программистов? 🤝\n\n"
    )
    while True:
        print("отправка опроса!")
        try:
            await asyncio.sleep(259200)
    # Отправка голосования
            await bot.send_poll(
                -1001929746261,
                question=msg,
                options=[
                    ' Да, я готов(а) выйти из своей пещеры и увидеть вас всех лично! 🥳', 
                    'Нет, я слишком увлечен(а) своим кодом, чтобы выходить на улицу. 🤓',
                    'Мне все равно, я доволен(а) как виртуальными, так и реальными встречами. 🤷‍♀️',
                ],
                type='regular',
                is_anonymous=True,
            )
            
        except Exception as e:
            logger.error(e)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    token = os.getenv('BOT_TOKEN')
    use_redis = False

    storage = RedisStorage2() if use_redis else MemoryStorage()
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await start()
        asyncio.create_task(send_posts(bot))
        asyncio.create_task(send_polly(bot))
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
