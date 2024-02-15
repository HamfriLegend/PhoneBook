import os
from PhoneBook import PhoneBook
import time
import re

book: PhoneBook = PhoneBook("PhoneBook.txt")
is_search: bool = False
records_id: list[int] = list(range(0, book.get_length()))
page: int = 1


def print_record(id_print_rec: int) -> None:
    """
    Функция вывода записи в консоль
    :param id_print_rec: ID Записи
    :return:
    """

    if id_print_rec < book.get_length() and id_print_rec >=0:
        record: dict[str, str] = book.get_data(id_print_rec)
        print(f"{id_print_rec}".center(6),
              f"{record['SurName']}".center(15),
              f"{record['Name']}".center(15),
              f"{record['MiddleName']}".center(15),
              f"{record['Organization']}".center(40),
              f"{record['WorkTelephone']}".center(15),
              f"{record['PersonTelephone']}".center(15), sep="|")


def search_record() -> None:
    """
    Функция указывающая, что в данном случае работает поиск
    :return:
    """

    print("Введите значения только тех полей по которым будет осуществляться поиск."
          "\nНе нужное пропустить нажатием Enter",
          "\nВведите 'cancel', чтобы отменить поиск")

    record_dict_for_search: dict[str, str] = {
        "Surname": "фамилию",
        "Name": "имя",
        "MiddleName": "отчество",
        "Organization": "название организации",
        "WorkTelephone": "рабочий телефон",
        "PersonTelephone": "личный телефон"
    }
    input_val_search: str = ""
    for key_rec_s, val_rec_s in record_dict_for_search.items():
        input_val_search = input(f"Введите {val_rec_s}: ").replace(',', '')
        if input_val_search == "cancel":
            break
        record_dict_for_search[key_rec_s] = input_val_search

    if input_val_search == "cancel":
        print("Поиск отменен")
        return

    global book
    global records_id
    records_id = book.search_phone_record(record_dict_for_search["Surname"],
                                          record_dict_for_search["Name"],
                                          record_dict_for_search["MiddleName"],
                                          record_dict_for_search["Organization"],
                                          record_dict_for_search["WorkTelephone"],
                                          record_dict_for_search["PersonTelephone"])
    global is_search
    is_search = True

    return


def is_correct_input(is_insert: bool = False) -> tuple[str, dict[str, str]]:
    """
    Функция проверки введенного значения
    :param is_insert: укажите True, если выполняется вставка (По умолчанию False)
    :return: 1) строка для проверки на отмену ('cancel')
             2) словарь введенных данных
    """
    record_dict: dict[str, str] = {
        "Surname": "фамилию",
        "Name": "имя",
        "MiddleName": "отчество",
        "Organization": "название организации",
        "WorkTelephone": "рабочий телефон",
        "PersonTelephone": "личный телефон"
    }
    input_val: str = ""
    for key_rec, val_rec in record_dict.items():
        correct: bool = False
        if input_val == "cancel":
            break
        while not correct:
            input_val = input(f"Введите {val_rec}: ").replace(',', '')
            if input_val == "cancel":
                break
            elif key_rec != "PersonTelephone" and key_rec != "WorkTelephone":
                if is_insert and input_val == "":
                    print("Вы ввели недопустимое значение")
                    time.sleep(1.5)
                    correct = False
                    continue
                else:
                    record_dict[key_rec] = input_val
                    correct = True
                    continue

            elif key_rec == "PersonTelephone" or key_rec == "WorkTelephone":
                input_val_without_number = re.sub(r'\d', '', input_val)
                if (input_val == "" or input_val_without_number != "") and is_insert:
                    print("Вы ввели недопустимое значение")
                    time.sleep(1.5)
                    correct = False
                    continue
                elif input_val == "" and input_val_without_number != "":
                    print("Вы ввели недопустимое значение")
                    time.sleep(1.5)
                    correct = False
                    continue
                else:
                    record_dict[key_rec] = input_val
                    correct = True
                    continue
    return input_val, record_dict


print("Это телефонный справочник, в котором содержится информация о:\n"
      "ФИО; Названии организации; Рабочего телефона; Личного телефона\n")

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Страница {page}")
    print("Номер".center(6),
          "Фамилия".center(15),
          "Имя".center(15),
          "Отчество".center(15),
          "Название организации".center(40),
          "Рабочий телефон".center(14),
          "Личный телефон".center(14), sep="|")

    for num_of_rec in range(10 * page - 10, 10 * page):
        if num_of_rec >= len(records_id):
            break
        print_record(records_id[num_of_rec])

    print("\nВыберите что вы хотите сделать:\n",
          "1 - Следующая страница;\n",
          "2 - Предыдущая страница;\n" if page > 1 else "",
          "3 - Добавить запись;\n",
          "4 - Редактировать запись;\n",
          "5 - Удалить запись;\n",
          "6 - Поиск записей;\n" if not is_search else "6 - Отменить поиск записей;", sep="")

    switch: str = input("Ваш вариант: ")

    if switch == "1":
        page += 1
        continue

    elif switch == "2":
        if page > 1:
            page -= 1

        else:
            print("Вы находитесь на первой странице!2")
        continue

    elif switch == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Введите 'cancel' чтобы отменить добавление записи")
        is_cancel: str
        record_dict_i: dict[str, str]
        is_cancel, record_dict_i = is_correct_input(True)

        if is_cancel == "cancel":
            print("Операция добавления отменена")
            time.sleep(1)
        else:
            book.insert_phone_record(record_dict_i["Surname"],
                                     record_dict_i["Name"],
                                     record_dict_i["MiddleName"],
                                     record_dict_i["Organization"],
                                     record_dict_i["WorkTelephone"],
                                     record_dict_i["PersonTelephone"])
            print("Запись добавлена")
            records_id = list(range(0, book.get_length()))
            is_search = False
            time.sleep(1)

    elif switch == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Введите 'cancel' чтобы отменить редактирование записи")
        while True:
            id_rec_edit = input("Введите номер записи: ")
            try:
                id_rec_edit = int(id_rec_edit)
            except ValueError:
                print("Вы ввели недопустимый номер")
                id_rec_edit = input("Введите номер записи: ")
            if id_rec_edit >= book.get_length() or id_rec_edit < 0:
                print("Вы ввели недопустимый номер")
                id_rec_edit = input("Введите номер записи: ")
            else:
                break

        is_cancel: str
        record_dict_e: dict[str, str]
        is_cancel, record_dict_e = is_correct_input(False)

        if is_cancel == "cancel":
            print("Операция редактирования отменена")
            time.sleep(1)
        else:
            book.edit_phone_record(id_rec_edit,
                                   record_dict_e["Surname"],
                                   record_dict_e["Name"],
                                   record_dict_e["MiddleName"],
                                   record_dict_e["Organization"],
                                   record_dict_e["WorkTelephone"],
                                   record_dict_e["PersonTelephone"])
            print("Запись изменена")
            time.sleep(1)

    elif switch == "5":
        while True:
            print("Введите 'cancel' чтобы отменить удаление записи")
            id_rec_del: str = input("Введите номер записи: ")
            if id_rec_del == "cancel":
                break
            try:
                book.remove_phone_record(int(id_rec_del))
                records_id = list(range(0, book.get_length()))
                is_search = False
                print("Удаление выполнено")
                time.sleep(1)
                break
            except ValueError:
                print("Вы ввели не верный номер")

        if id_rec_del == "cancel":
            print("Удаление отменено")
            time.sleep(1)

    elif switch == "6":
        if not is_search:
            search_record()
            page = 1
        else:
            is_search = False
            records_id = list(range(0, book.get_length()))
            page = 1
