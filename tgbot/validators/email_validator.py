import re


async def validate_email(email):
    # Регулярное выражение для проверки формата email-адреса
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Проверка соответствия email-адреса регулярному выражению
    if re.match(pattern, email):
        return True
    else:
        return False
