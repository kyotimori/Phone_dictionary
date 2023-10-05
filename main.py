import json

# Словарь для сопоставления названий полей в справочнике и названия столбцов для пользователя
field_names = {"name": "Имя",
               "surname": "Фамилия",
               "patronymic": "Отчество",
               "organization_name": "Название организации",
               "work_phone": "Рабочий телефон",
               "personal_phone": "Личный телефон",
               "id": "id"}
# Ширина колонок выводимой таблицы
col_width = 25


def print_table_header() -> None:
    """Вывод шапки таблицы"""
    for field in field_names.values():
        print(field.ljust(col_width), end='')
    print()


def get_existing_data(filename) -> str:
    """Получение существующих записей из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return "В справочнике пока нет записей"


def validate_data(field, data) -> bool:
    """Проверка корректности данных"""
    if field == 'work_phone' or field == 'personal_phone':
        for sym in data:
            if not sym.isdigit():
                print("Номер телефона должен состоять из цифр")
                return False
        return True
    elif field != 'organization_name':
        for sym in data:
            if not sym.isalpha():
                print("ФИО должно содержать только буквы")
                return False
        return True
    else:
        return True


def get_data(filename) -> None:
    """Вывод всех записей из файла на экран"""
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            if not existing_data:
                print("В справочнике пока нет записей")
                return
            print_table_header()
            for row in existing_data:
                for field in row.values():
                    print(str(field).ljust(col_width), end='')
                print()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("В справочнике пока нет записей")
        return


def add_data(filename) -> None:
    """Добавление новой записи в файл"""
    new_data = {
        "name": "",
        "surname": "",
        "patronymic": "",
        "organization_name": "",
        "work_phone": "",
        "personal_phone": ""
    }
    # Ввод данных новой записи
    for field in new_data.keys():
        data = input(f"{field_names[field]}: ")
        while not validate_data(field, data):
            data = input(f"{field_names[field]}: ")
        new_data[field] = data.title()

    # Получение существующих записей
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            if not existing_data:
                existing_data = []
                new_data["id"] = 1
            else:
                new_id = existing_data[-1]["id"] + 1
                new_data["id"] = new_id
    except json.decoder.JSONDecodeError:
        existing_data = []
        new_data["id"] = 1
    except FileNotFoundError:
        existing_data = []
        new_data["id"] = 1
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file)

    existing_data.append(new_data)

    # Запись новых данных в файл
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4)


def edit_data(filename) -> None:
    """Редактирование существующей записи"""
    # Получение существующих записей
    existing_data = get_existing_data(filename)

    while True:
        # Получение записи для редактирования
        index = input("Введите id записи для редактирования: ")
        if index.isdigit() and 1 <= int(index) <= len(existing_data):
            current_row = existing_data[int(index) - 1]

            # Изменение данных
            print("Введите новые данные")
            for field in current_row.keys():
                if field == "id":
                    continue
                data = input(f"{field_names[field]}: ")
                while not validate_data(field, data):
                    data = input(f"{field_names[field]}: ")
                current_row[field] = data

            # Обновление данных в файле
            existing_data[int(index) - 1] = current_row
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, indent=4)
            break
        else:
            print("Некорректный ввод")


def search_data(filename) -> None:
    """Поиск записей по одной или нескольким характеристикам"""
    # Получение существующих записей
    existing_data = get_existing_data(filename)

    # Поиск соответствий
    result = set()
    target = input("Введите информацию для поиска: ")
    for row in existing_data:
        for field in row.values():
            if target.lower() in str(field).lower():
                result.add(row["id"])

    # Вывод результатов
    if not result:
        print("Ничего не найдено")
        return

    print("Результаты поиска:")
    print_table_header()
    for elem in result:
        for field in existing_data[elem - 1].values():
            print(str(field).ljust(col_width), end='')
        print()


if __name__ == '__main__':
    filename = 'book.json'
    options = {"1": get_data, "2": add_data, "3": edit_data, "4": search_data}
    while True:
        option = input("Выберите опцию:\n"
                       "1 - Вывод постранично записей из справочника на экран\n"
                       "2 - Добавление новой записи в справочник\n"
                       "3 - Редактирование существующей записи\n"
                       "4 - Поиск записей\n"
                       "Введите exit для выхода из программы\n")
        if option == "exit":
            break
        if not options.get(option):
            print("Некорректный ввод")
        else:
            options[option](filename)
