import os
from pathlib import Path


class PhoneBook:
    """
    Класс, предназначенный для хранения и работы с телефонной книгой
    """
    __phoneData: list[str]
    __fileName: str

    def __init__(self, phoneBookFileName: str) -> None:
        self.__fileName = phoneBookFileName
        if not os.path.exists(phoneBookFileName):
            Path(phoneBookFileName).touch()

        with open(phoneBookFileName, 'r', encoding='utf-8') as file:
            self.__phoneData = [line.strip('\n') for line in file if line.strip('\n') != ""]


    def get_length(self) -> int:
        """
        Функция для получения количества записей
        :return: Кол-во записей
        """
        return len(self.__phoneData)

    def get_data(self, id_rec: int) -> dict[str, str]:
        """
        Функция, которая возвращает запись из книги в виде словаря
        :param id_rec: id записи из книги
        :return: Словарь {SurName,Name,MiddleName,Organization,WorkTelephone,PersonTelephone}
        """
        record_data: list[str] = self.__phoneData[id_rec].split(',')
        if len(record_data) != 0:
            dict_data: dict[str, str] = {"SurName": record_data[0],
                                         "Name": record_data[1],
                                         "MiddleName": record_data[2],
                                         "Organization": record_data[3],
                                         "WorkTelephone": record_data[4],
                                         "PersonTelephone": record_data[5]}
        return dict_data

    def insert_phone_record(self, surName: str, name: str,
                            middleName: str, organization: str,
                            workTelephone: str, personTelephone: str) -> None:
        """
        Функция для добавления новой записи в книгу
        :param surName: Фамилия
        :param name: Имя
        :param middleName: Отчество
        :param organization: Название организации
        :param workTelephone: Рабочий телефон
        :param personTelephone: Личный телефон
        :return:
        """
        self.__phoneData.append(",".join([surName, name, middleName, organization, workTelephone, personTelephone]))
        self._save_phone_data()

    def _save_phone_data(self) -> None:
        """
        Функция сохранения данных в файл
        :return:
        """
        with open(self.__fileName, 'w') as file:
            for record in self.__phoneData:
                file.write(record + '\n')

    def remove_phone_record(self, id_rec: int) -> None:
        """
        Функция удаления записи из книги
        :param id_rec: id записи
        :return:
        """
        if id_rec < 0 or id_rec >= self.get_length():
            raise ValueError(f"id должен быть больше или равен 0 и меньше {self.get_length()} \n id_rec={id_rec}")
        self.__phoneData.pop(id_rec)
        self._save_phone_data()

    def search_phone_record(self, surName: str = "", name: str = "",
                            middleName: str = "", organization: str = "",
                            workTelephone: str = "", personTelephone: str = "") -> list[int]:
        """
        Функция для поиска записей из книги
        :param surName: Фамилия
        :param name: Имя
        :param middleName: Отчество
        :param organization: Название организации
        :param workTelephone: Рабочий телефон
        :param personTelephone: Личный телефон
        :return: Список id записей
        """
        list_of_id_records: list[int] = list()
        for id_rec in range(0, self.get_length()):
            record_data: list[str] = self.__phoneData[id_rec].split(',')
            if (surName.lower() in record_data[0].lower()
                    and name.lower() in record_data[1].lower()
                    and middleName.lower() in record_data[2].lower()
                    and organization.lower() in record_data[3].lower()
                    and workTelephone.lower() in record_data[4].lower()
                    and personTelephone.lower() in record_data[5].lower()):
                list_of_id_records.append(id_rec)

        return list_of_id_records

    def edit_phone_record(self, id_rec: int, surName: str = "", name: str = "",
                          middleName: str = "", organization: str = "",
                          workTelephone: str = "", personTelephone: str = "") -> None:
        """
        Функция для редактирования записи в книгу
        :param id_rec: ID редактируемой записи
        :param surName: Фамилия
        :param name: Имя
        :param middleName: Отчество
        :param organization: Название организации
        :param workTelephone: Рабочий телефон
        :param personTelephone: Личный телефон
        :return: Список id записей
        """
        if id_rec < 0 or id_rec >= self.get_length():
            raise ValueError(f"id должен быть больше или равен 0 и меньше {self.get_length()} \n id_rec={id_rec}")
        else:
            record_dict: list[str] = self.__phoneData[id_rec].split(',')
            self.__phoneData[id_rec] = ",".join(
                [surName if surName != "" else record_dict[0],
                 name if name != "" else record_dict[1],
                 middleName if middleName != "" else record_dict[2],
                 organization if organization != "" else record_dict[3],
                 workTelephone if workTelephone != "" else record_dict[4],
                 personTelephone if personTelephone != "" else record_dict[5]])
            self._save_phone_data()
