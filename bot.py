import telebot
from values import keys
from extensions import APIException,CryptoConverter

# получаем токен из другого файла (в репозиторий не загружен)
with open('token.txt') as token_file:
    Token=token_file.read()

bot=telebot.TeleBot(Token)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text=f'Добрый день, {message.chat.username}!\nДля работы введите команду в следующем формате: \n<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nИнформация обо всех доступных валютах: /values'
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:\n'
    for key in keys.keys():
        text='\n'.join((text,key, ))
    bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = (message.text.lower()).split()   # приведем все введенные символы в нижний регистр для удобства обработки
        if len(values)==2:
            values.append(1)  # если количество валюты не введено, предполагаем, что нужно узнать цену одной единицы валюты
        if len(values)==1 or len(values)>3:
            raise APIException('Для корректной работы бота необходимо ввести три параметра\nОбразец: доллар рубль 6')

        base,quote,amount = values
        ending_base=""
        ending_quote=""
        total_base=CryptoConverter.get_price(base,quote,amount)
    except APIException as e:
        bot.send_message(message.chat.id,f'Ошибка ввода данных\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id,f'Возникла непредвиденная ошибка\n{e}')
    else: # меняем окончания выводимых валют в зависимости от введенного числа-количества
        if base=='рубль':
            base=base[0:4]
            if (float(amount)%10)==1:
                ending_base='я'
            if (float(amount)%10)in range(2,10):
                ending_base='ей'
        if base in ['доллар','биткоин','эфириум']:
            if (float(amount)%10)==1:
                ending_base='а'
            if (float(amount)%10) in range(2,10):
                ending_base = 'ов'
        if base=='йена':
            if (float(amount)%10)==1:
                base=base[0:3]
                ending_base='ы'
            if (float(amount)%10) in range(2,10):
                base = base[0:3]
        if quote=='рубль':
            quote=quote[0:4]
            ending_quote='ях'
        if quote in ['доллар','биткоин','эфириум','йена']:
            if quote=='йена':
                quote = quote[0:3]
            ending_quote ='ах'

        text=f'Цена {amount} {base}{ending_base} в {quote}{ending_quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()