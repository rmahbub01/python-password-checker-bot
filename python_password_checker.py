from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import requests
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code} please check again')
    return response

def read_response(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0




def api_pwned(password):
    sha_pass = hashlib.sha1(password.encode('utf_8')).hexdigest().upper()
    first5 , tail = sha_pass[:5],sha_pass[5:]
    response = request_api_data(first5)
    return read_response(response,tail)

def print_chat(update:Update,context:CallbackContext):
    text = update.message.text
    password = ''
    if '/check' in text:
        password = text.split()[1].strip()
        count = api_pwned(password)
        if count:
            update.message.reply_text(f'Your Password: {password} has been hacked {count} times.....\nPlease Change Your Password')
        else:
            update.message.reply_text(f'Your Password: {password} is Safe. Congratulations!!!')


def main():
    updater = Updater(token='1438893616:AAEUrzCQs1UmET8H_Ls4cArC_IvWZtnFTUA',use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.command,print_chat))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
