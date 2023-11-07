import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


CONFIRM_MUTE = 1


def start_mute(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.user_data['user_to_mute'] = user
    update.message.reply_text(f"Вы хотите замутить {user.first_name} {user.last_name} (@{user.username})? (Да/Нет)")

    return CONFIRM_MUTE


def confirm_mute(update: Update, context: CallbackContext) -> int:
    user = context.user_data.get('user_to_mute')
    response = update.message.text.lower()
    if response == 'да':

        update.message.reply_text(f"{user.first_name} {user.last_name} (@{user.username}) замучен на время.")
    else:
        update.message.reply_text("Мут не был выполнен.")

    return ConversationHandler.END


def handle_text(update: Update, context: CallbackContext):
    pass



def main():

    updater = Updater(token='6016018942:AAFUVgIoCD6dW5piIy55q2HArjKZ4hlgbDs', use_context=True)
    dp = updater.dispatcher


    dp.add_handler(CommandHandler('mute', start_mute))


    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    #
    conv_handler = ConversationHandler(
        entry_points=[],
        states={
            CONFIRM_MUTE: [MessageHandler(Filters.text, confirm_mute)]
        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)

    #
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
