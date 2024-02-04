import datetime
import json
from pathlib import Path


def unpacking_json(json_file):
    """
    распаковка json
    """
    try:
        with open(json_file) as file:
            raw_json = file.read()
            operations = json.loads(raw_json)
            return operations

    except FileNotFoundError:
        return 'Файл не найден'


def sort_operations():
    """
    :return: отсортированный список последних 5 операций
    """
    file_json = Path.home() / 'PycharmProjects' / 'account_transactions' / 'code_account' / 'operations.json'
    operations = unpacking_json(file_json)
    operations_list = [operation for operation in operations if operation.get('state') == 'EXECUTED']
    sort_operations_list = sorted(operations_list, key=lambda x: x['date'], reverse=True)
    return sort_operations_list[:5]


def correct_date(date: str) -> object:
    """
    :param date: Дата операции
    :return: дату операции в формате ДД.ММ.ГГГГ
    """
    cor_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    return f"{cor_date:%d.%m.%Y}"


def masking_card(card_num: str) -> object:
    """
    :param card_num: номер карты или счета
    :return: зашифрованный номер карты или счета
    """
    card_num_list = card_num.split()
    if len(card_num_list[-1]) == 16:
        return (' '.join(card_num_list[:-1]) + " " + card_num_list[-1][:4] + " " + card_num_list[-1][4:6] + "**" +
                " " + "****" + " " + card_num_list[-1][12:])
    elif len(card_num_list[-1]) == 20:
        return ' '.join(card_num_list[:-1]) + " " + "**" + card_num_list[-1][16:]


def print_of_operations(sorted_operations):
    """
    :return: Вывод операций на печать
    """
    sort_operations_list = []
    for operation in sorted_operations:
        if "from" in operation:
            sort_operations_list.append(f'''{correct_date(operation["date"])} {operation["description"]}
{masking_card(operation["from"])} -> {masking_card(operation["to"])}
{operation["operationAmount"]["amount"]} {operation["operationAmount"]["currency"]["name"]}''')
        else:
            sort_operations_list.append(f'''{correct_date(operation["date"])} {operation["description"]}
{masking_card(operation["to"])}
{operation["operationAmount"]["amount"]} {operation["operationAmount"]["currency"]["name"]}''')
    return '\n\n'.join(sort_operations_list)
