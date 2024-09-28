from transliterate import get_translit_function
from itertools import permutations

DICT_DIGIT_CHANGE_SYMBOL = {'0': 'о', '3': 'з', 'ё': 'е'}
DICT_SYMBOL_CHANGE_DIGIT = {'о': '0', 'з': '3'}
LIST_NATIONAL_FATHER = ('ОГЛЫ', 'КЫЗЫ', 'УГЛИ', 'ОГЛУ', 'УУЛУ', 'ЗАДЕ', 'ХАН', 'БАБА')
LIST_CANCEL = ('ОТСУТСТВУЕТ', 'НЕТ')


def _one_date(num: str) -> str:
    if 1900 <= int(num) <= 2024:
        return num
    if len(num) == 4:
        if 1900 <= int('1' + num[1:]) <= 2024:
            return '1' + num[1:]
        if 1900 <= int('2' + num[1:]) <= 2024:
            return '2' + num[1:]
        if int(num[2:]) > 24:
            return '19' + num[2:]
        return '20' + num[2:]
    if len(num) == 3:
        if 1900 <= int('1' + num) <= 2024:
            return '1' + num
        if 1900 <= int('2' + num) <= 2024:
            return '2' + num
        if int(num[1:]) > 24:
            return '19' + num[1:]
        return '20' + num[1:]
    if len(num) == 2:
        if int(num) > 24:
            return '19' + num
        return '20' + num
    if len(num) == 1:
        return '199' + num
    return num


def _last_date(num: str, ogr: int) -> str:
    if len(num) == 2:
        if 1 <= int(num) <= ogr:
            return num
        if 1 <= int(num[::-1]) <= ogr:
            return num[::-1]
        return '0' + num[1]
    if len(num) == 1:
        if int(num) == 0:
            return '01'
        return '0' + num
    return num


def translate(s: str, rev=False) -> str:
    func = get_translit_function('ru')
    return func(s, reversed=rev)


def normal_word(word: str) -> str:
    new_word = ''
    flag_no_russian_char = False
    for c in word:
        if c in DICT_DIGIT_CHANGE_SYMBOL:
            new_word += DICT_DIGIT_CHANGE_SYMBOL[c]
        elif c.isalpha():
            new_word += c.upper()
            if not ('А' <= new_word[-1] <= 'Я'):
                flag_no_russian_char = True
    if flag_no_russian_char:
        return translate(new_word)
    return new_word


def normal_fio(fio: str) -> str:
    new_fio = []
    for w in fio.split():
        word = normal_word(w)
        if word not in LIST_NATIONAL_FATHER and word not in new_fio and word not in LIST_CANCEL:
            new_fio.append(word)
    return ' '.join(new_fio)


def normal_email(address: str) -> str:  # вопрос с литерацией адресов
    new_addrress = ''
    flag_no_english_char = False
    for c in address:
        if c.isalpha() or c.isdigit():
            new_addrress += c.lower()
            if not ('a' <= new_addrress[-1] <= 'z'):
                flag_no_english_char = True
    if flag_no_english_char:
        return translate(new_addrress, rev=True)
    return new_addrress


def normal_mobile_phone(phone: str) -> str:
    new_phone = ''
    for d in phone:
        if d.isdigit() or d == '+':
            new_phone += d
        elif d in DICT_SYMBOL_CHANGE_DIGIT:
            new_phone += DICT_SYMBOL_CHANGE_DIGIT[d]
    if new_phone.startswith('+7'):
        new_phone = new_phone.replace('+7', '8', 1)
    new_phone.replace('+', '')
    return new_phone


def normal_date(date: str) -> str:
    datatime = date.split('-')
    if len(datatime) == 3:
        return _one_date(datatime[0]) + '-' + _last_date(datatime[1], 31) + '-' + _last_date(datatime[2], 12)
    return date

def normal_address(address: str) -> str:
    flag_no_russian_char = False
    new_address = ''
    ln = len(address)
    for i in range(ln):
        if address[i] in DICT_DIGIT_CHANGE_SYMBOL and (1 <= i <= ln - 2):
            if address[i - 1].isalpha() and address[i + 1].isalpha():
                new_address += DICT_DIGIT_CHANGE_SYMBOL[address[i]]
            else:
                new_address += address[i].lower()
        elif address[i] in DICT_SYMBOL_CHANGE_DIGIT and (1 <= i <= ln - 2):
            if address[i - 1].isdigit() and address[i + 1].isdigit():
                new_address += DICT_SYMBOL_CHANGE_DIGIT[address[i]]
            else:
                new_address += address[i].lower()
        elif address[i].isalpha() or address[i].isdigit() or address[i] == ' ':
            new_address += address[i].lower()
            if not (('а' <= new_address[-1] <= 'я') or new_address[-1] == ' '):
                flag_no_russian_char = True
    if flag_no_russian_char:
        return translate(new_address)
    return new_address

