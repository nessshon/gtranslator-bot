class Text:
    strings = {
        "en": {
            "start": (
                "<b>Hi {}!</b>\n\n"
                "Telegram bot translator, based on google translation interface.\n\n"
                "<b>Select language and send text:</b>\n"
                "<i>Symbols limit 3000.</i>"
            ),
            "source": (
                "https://github.com/nessshon/google-translator-bot"
            ),
            "translate": (
                "<b>Select language and send text:</b>\n"
            ),
            "language": (
                "<b>Choose language:</b>"
            )
        },
        "ru": {
            "start": (
                "<b>Привет {}!</b>\n\n"
                "Telegram Бот переводчик, основанный на Google Translate.\n\n"
                "<b>Выберите язык и отправьте текст:</b>\n"
                "<i>Ограничение на количество символов 3000.</i>"
            ),
            "source": (
                "https://github.com/nessshon/google-translator-bot"
            ),
            "translate": (
                "<b>Выберите язык и отправьте текст:</b>\n"
            ),
            "language": (
                "<b>Выберите язык:</b>"
            )
        }
    }

    def __init__(self, language: str):
        self.language = language

    def get(self, key: str) -> str:
        return self.strings[self.language][key]
