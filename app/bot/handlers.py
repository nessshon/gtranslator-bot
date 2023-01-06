import logging

from aiogoogletrans import Translator

from aiogram import Dispatcher
from aiogram.utils.markdown import hcode
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, User

from .texts import Text
from .states import UserState
from .filters import IsPrivate

from .keyboards import CallbackData
from .keyboards import current_languages_markup, choose_language_markup

from .misc.languages import SUPPORT_LANGUAGES
from .misc.throttling import rate_limit, waiting_previous_execution
from .misc.messages import edit_message, delete_message, delete_previous_message


async def translate_message(state: FSMContext,
                            message: Message = None,
                            call: CallbackQuery = None,
                            translated_text: str = None):
    data = await state.get_data()

    translate_to = data["translate_to"]
    translate_from = data["translate_from"]

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    text = Text(language_code).get("translate")
    markup = current_languages_markup(
        language_code=language_code,
        translate_from=translate_from,
        translate_to=translate_to
    )

    if translated_text:
        await edit_message(message, hcode(translated_text))
    if message:
        msg = await message.answer(text, reply_markup=markup)
        await state.update_data(message_id=msg.message_id)
    else:
        await edit_message(call.message, text, reply_markup=markup)

    await UserState.TRANSLATE.set()


async def choose_language(state: FSMContext,
                          message: Message = None,
                          call: CallbackQuery = None):
    data = await state.get_data()

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    text = Text(language_code).get("language")
    markup = choose_language_markup(language_code)

    if message:
        await message.answer(text, reply_markup=markup)
    else:
        await edit_message(call.message, text, reply_markup=markup)

    if data["toggle"] == "FROM":
        await UserState.TRANSLATE_FROM.set()
    else:
        await UserState.TRANSLATE_TO.set()


@rate_limit(1)
@waiting_previous_execution
async def translate_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    translate_to = data["translate_to"]
    translate_from = data["translate_from"]

    if message.content_type == "text" and len(message.text) <= 3000:
        emoji = await message.reply("⌛️")
        await state.update_data(throttling=True)
        await delete_previous_message(message, state)

        try:
            translated = await Translator().translate(
                text=message.text,
                dest=translate_to,
                src=translate_from
            )
            await translate_message(state, message=emoji, translated_text=translated.text)
        except Exception as e:
            logging.error(e)
        finally:
            await state.update_data(throttling=False)
    else:
        await delete_message(message)


@rate_limit(0.5)
async def translate_message_callback_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    translate_to = data["translate_to"]
    translate_from = data["translate_from"]

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    if call.data == CallbackData.CHANGE:
        await state.update_data(
            translate_from=translate_to,
            translate_to=translate_from
        )
        await translate_message(state, call=call)
    else:
        toggle, language = call.data.split(":")

        if language in SUPPORT_LANGUAGES[language_code].keys():
            await state.update_data(toggle=toggle)
            await choose_language(state, call=call)

    await call.answer()


@rate_limit(0.5)
async def choose_language_callback_handler(call: CallbackQuery, state: FSMContext):
    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    if call.data == CallbackData.BACK:
        await translate_message(state, call=call)

    elif call.data in SUPPORT_LANGUAGES[language_code].keys():
        if await state.get_state() == UserState.TRANSLATE_TO.state:
            await state.update_data(translate_to=call.data)
        else:
            await state.update_data(translate_from=call.data)
        await translate_message(state, call=call)

    await call.answer()


def register(dp: Dispatcher):
    dp.register_message_handler(
        translate_message_handler, IsPrivate(),
        state=UserState.TRANSLATE,
        content_types="any"
    )
    dp.register_callback_query_handler(
        translate_message_callback_handler, IsPrivate(),
        state=UserState.TRANSLATE
    )
    dp.register_callback_query_handler(
        choose_language_callback_handler, IsPrivate(),
        state=[UserState.TRANSLATE_TO, UserState.TRANSLATE_FROM]
    )
