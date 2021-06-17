import csv
import os


def searcher():
    # Возвращает полный путь последнего созданного в папке "Загрузки" файла
    path = 'path'  # путь к папке, в которую скачиваются лиды
    files = os.listdir(path)
    if files:
        files = [os.path.join(path, file) for file in files]
        files = [file for file in files if os.path.isfile(file)]  # оставляет в списке только файлы

    lastest_file = max(files, key=os.path.getctime)
    return lastest_file


def leads_sheet_creator():
    # Возвращает список лидов из заданного файла
    filename = searcher()
    try:
        with open(filename, encoding='utf-16') as f:
            reader = csv.reader(f, delimiter='\t')
            header_row = next(reader)
            index_name = header_row.index("имя")
            index_form_name = header_row.index("form_name")
            try:
                index_telephone = header_row.index("номер_телефона")
            except ValueError:
                index_telephone = header_row.index("телефонный_номер")
            leads_sheet = ""
            for row in reader:
                leads_sheet += f"{row[index_name]}, {row[index_telephone]} - {row[index_form_name]}\n"

            if leads_sheet == "":
                leads_sheet = "Лиды не обнаружены"
    except UnicodeDecodeError:
        with open(filename) as f:
            reader = csv.reader(f, delimiter='\t')
            header_row = next(reader)
            index_name = header_row.index("имя")
            index_form_name = header_row.index("form_name")
            try:
                index_telephone = header_row.index("номер_телефона")
            except ValueError:
                index_telephone = header_row.index("телефонный_номер")
            leads_sheet = ""
            for row in reader:
                leads_sheet += f"{row[index_name]}, {row[index_telephone]} - {row[index_form_name]}\n"

            if leads_sheet == "":
                leads_sheet = "Лиды не обнаружены"

    os.remove(filename)

    return leads_sheet
