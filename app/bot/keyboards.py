from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .misc.languages import SUPPORT_LANGUAGES


@dataclass
class CallbackData:
    BACK: str = "BACK"
    CHANGE: str = "CHANGE"
    FROM: str = "FROM:"
    TO: str = "TO:"


def current_languages_markup(language_code: str,
                             translate_from: str,
                             translate_to: str
                             ) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)

    markup.add(
        InlineKeyboardButton(
            text=SUPPORT_LANGUAGES[language_code].get(translate_from),
            callback_data=CallbackData.FROM + translate_from
        ),
        InlineKeyboardButton(
            text="⇌", callback_data=CallbackData.CHANGE
        ),
        InlineKeyboardButton(
            text=SUPPORT_LANGUAGES[language_code].get(translate_to),
            callback_data=CallbackData.TO + translate_to
        )
    )
    return markup


def choose_language_markup(language_code: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)

    markup.add(
        *[
            InlineKeyboardButton(
                text=language, callback_data=language_code
            ) for language_code, language in
            SUPPORT_LANGUAGES[language_code].items()
        ],
        InlineKeyboardButton(
            text="←", callback_data=CallbackData.BACK
        )
    )
    return markup
