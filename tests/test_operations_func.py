import pytest

from code_account.operations_func import (unpacking_json, sort_operations, correct_date, masking_card,
                                          print_of_operations)

operations = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code_account": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code_account": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    },
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code_account": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }]


def test_unpacking_json():
    assert (unpacking_json("/home/tatianat/PycharmProjects/account_transactions/code_account/operations.json")[0]["id"]
            == 441945886)
    assert unpacking_json("operation.json") == 'Файл не найден'


def test_sort_operations():
    sorted_operations = sort_operations()
    assert sorted_operations[0]['date'] == "2019-12-08T22:46:21.935582"
    assert sorted_operations[1]['state'] == 'EXECUTED'
    assert sorted_operations[0]['id'] == 863064926


def test_correct_date():
    assert correct_date(operations[0]['date']) == '26.08.2019'


@pytest.mark.parametrize('card, expected', [
    (operations[0]['from'], 'Maestro 1596 83** **** 5199'),
    (operations[1]['from'], 'MasterCard 7158 30** **** 6758'),
    (operations[2]['from'], 'Счет **6952')
])
def test_masking_card(card, expected):
    assert masking_card(card) == expected


def test_print_operations():
    assert print_of_operations(operations) == ('26.08.2019 Перевод организации\n'
                                               'Maestro 1596 83** **** 5199 -> Счет **9589\n'
                                               '31957.58 руб.\n'
                                               '\n'
                                               '03.07.2019 Перевод организации\n'
                                               'MasterCard 7158 30** **** 6758 -> Счет **5560\n'
                                               '8221.37 USD\n'
                                               '\n'
                                               '30.06.2018 Перевод организации\n'
                                               'Счет **6952 -> Счет **6702\n'
                                               '9824.07 USD')
