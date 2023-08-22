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


# Вывод шапки таблицы
def print_table_header():
    for field in field_names.values():
        print(field.ljust(col_width), end='')
    print()


# Получение существующих записей
def get_existing_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return "В справочнике пока нет записей"


# Проверка корректности номера, можно также добавить проверку на длину или, например, код страны
def check_phone(phone):
    for sym in phone:
        if not sym.isdigit():
            return False
    return True


# Вывод всех записей на экран
def get_data(filename):
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


# Добавление новой записи
def add_data(filename):
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
        temp = input(f"{field_names[field]}: ")
        if field == "work_phone" or field == "personal_phone":
            while not check_phone(temp):
                print("Некорректный номер телефона")
                temp = input(f"{field_names[field]}: ")
        new_data[field] = temp

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


# Редактирование записи
def edit_data(filename):
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
                temp = input(f"{field_names[field]}: ")
                if field == "work_phone" or field == "personal_phone":
                    while not check_phone(temp):
                        print("Некорректный номер телефона")
                        temp = input(f"{field_names[field]}: ")
                current_row[field] = temp

            # Обновление данных в файле
            existing_data[int(index) - 1] = current_row
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, indent=4)
            break
        else:
            print("Некорректный ввод")


# Поиск записей по одной или нескольким характеристикам
def search_data(filename):
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
