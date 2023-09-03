from aiogram.utils.markdown import hide_link


class Text:
    strings = {
        "en": {
            "start": (
                f"{hide_link('https://telegra.ph//file/c23cf9899e97d2dd731db.jpg')}"
                "<b>Hi {}!</b>\n\n"
                "Telegram bot translator, based on google translation interface.\n\n"
                "<b>Select language and send text:</b>\n\n"
                "• Symbols limit 3000."
            ),
            "source": (
                "https://github.com/nessshon/google-translator-bot"
            ),
            "translate": (
                f"{hide_link('https://telegra.ph//file/c23cf9899e97d2dd731db.jpg')}"
                "<b>Select language and send text:</b>\n\n"
                "• Symbols limit 3000."
            ),
            "language": (
                f"{hide_link('https://telegra.ph//file/c23cf9899e97d2dd731db.jpg')}"
                "<b>Choose language:</b>"
            )
        },
        "ru": {
            "start": (
                f"{hide_link('https://telegra.ph//file/64794614a4c2c42122ac8.jpg')}"
                "<b>Привет {}!</b>\n\n"
                "Telegram Бот переводчик, основанный на Google Translate.\n\n"
                "<b>Выберите язык и отправьте текст:</b>\n\n"
                "• Ограничение на количество символов 3000."
            ),
            "source": (
                "https://github.com/nessshon/google-translator-bot"
            ),
            "translate": (
                f"{hide_link('https://telegra.ph//file/64794614a4c2c42122ac8.jpg')}"
                "<b>Выберите язык и отправьте текст:</b>\n\n"
                "• Ограничение на количество символов 3000."
            ),
            "language": (
                f"{hide_link('https://telegra.ph//file/64794614a4c2c42122ac8.jpg')}"
                "<b>Выберите язык:</b>"
            )
        }
    }

    def __init__(self, language: str):
        self.language = language

    def get(self, key: str) -> str:
        return self.strings[self.language][key]
