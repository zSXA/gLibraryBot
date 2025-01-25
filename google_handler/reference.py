from gspread import Client, Spreadsheet, Worksheet, service_account, exceptions
from typing import List, Dict
from faker import Faker

table_url = "https://docs.google.com/spreadsheets/d/1qPdi8-dwzekVP1vxE_7mRMtacn_LgcxjZHI_nvV7NMw/"
table_key = "1qPdi8-dwzekVP1vxE_7mRMtacn_LgcxjZHI_nvV7NMw"

def generate_fake_user():
    fake = Faker('ru-RU')

    return {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'birth_date': fake.date_of_birth().strftime("%d.%m.%Y"),
        'company': fake.company(),
        'job': fake.job()
    }

def get_fake_users(count: int) -> List:
    return [generate_fake_user() for _ in range(count)]

def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='glibrarybot-014a8a5f400f.json')

def get_table_by_url(client: Client, table_url):
    """Получение таблицы из Google Sheets по ссылке."""
    return client.open_by_url(table_url)

def get_table_by_key(client: Client, table_key):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_key)

def get_worksheet_info(table: Spreadsheet) -> dict:
    """Возвращает количество листов в таблице и их названия."""
    worksheets = table.worksheets()
    worksheet_info = {
        "count": len(worksheets),
        "names": [worksheet.title for worksheet in worksheets]
    }
    return worksheet_info

def create_worksheet(table: Spreadsheet, title: str, rows: int, cols: int):
    """Создание листа в таблице."""
    return table.add_worksheet(title, rows, cols)

def delete_worksheet(table: Spreadsheet, title: str):
    """Удаление листа из таблицы."""
    return table.del_worksheet(table.worksheet(title))

def insert_one(table: Spreadsheet, title: str, data: list, index: int = 1):
    """Вставка данных в лист."""
    worksheet = table.worksheet(title)
    worksheet.insert_row(data, index=index)

def extract_data_from_sheet(table: Spreadsheet, sheet_name: str) -> List[Dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    rows = worksheet.get_all_records()
    return rows

def extract_data_from_sheet_var_2(table: Spreadsheet, sheet_name: str) -> List[Dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    headers = worksheet.row_values(1)  # Первая строка считается заголовками

    data = []
    rows = worksheet.get_all_values()[1:]  # Начинаем считывать с второй строки

    for row in rows:
        row_dict = {headers[i]: value for i, value in enumerate(row)}
        data.append(row_dict)

    return data

def clear_range(table: Spreadsheet, sheet_name: str, start_cell: str, end_cell: str) -> None:
    """
    Удаляет данные из заданного диапазона ячеек на указанном рабочем листе таблицы Google Sheets.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :param start_cell: Начальная ячейка диапазона (например, 'A1').
    :param end_cell: Конечная ячейка диапазона (например, 'B10').
    """
    worksheet = table.worksheet(sheet_name)
    cell_list = worksheet.range(f"{start_cell}:{end_cell}")
    for cell in cell_list:
        cell.value = ''
    worksheet.update_cells(cell_list)
    print(f"Данные в диапазоне {start_cell}:{end_cell} на листе '{sheet_name}' были успешно удалены.")

def clear_sheet(table: Spreadsheet, sheet_name: str) -> None:
    """
    Удаляет все данные из указанного рабочего листа таблицы Google Sheets.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    """
    worksheet = table.worksheet(sheet_name)
    worksheet.clear()
    print(f"Все данные на листе '{sheet_name}' были успешно удалены.")

# ===========================================
# Референсы как создавать, обновлять и удалять

def test_get_table(table_url: str, table_key: str):
    """Тестирование полчения таблицы из Google Sheets."""
    client = client_init_json()
    table = get_table_by_url(client, table_url)
    print('Инфо по таблице по ссылке: ', table)
    table = get_table_by_key(client, table_key)
    print('Инфо по таблице по id: ', table)

def test_create_worksheet():
    client = client_init_json()
    table = get_table_by_key(client, table_key)
    rez = create_worksheet(table, 'НовыйРабочийЛист', rows=15, cols=10)
    print(rez)

def test_add_data():
    """Тестирование добавления данных в таблицу."""
    client = client_init_json()
    table = get_table_by_key(client, table_key)
    worksheet_info = get_worksheet_info(table)
    print('Инфо по таблице: ', worksheet_info)
    insert_one(table=table,
               title=worksheet_info['names'][0],
               data=['name', 'address', 'email', 'phone_number', 'birth_date', 'company', 'job'])

def add_data_to_worksheet_var_1(table: Spreadsheet, title: str, data: List[Dict], start_row: int = 2) -> None:
    """
    Добавляет данные на рабочий лист в Google Sheets.

    :param table: Объект таблицы (Spreadsheet).
    :param title: Название рабочего листа.
    :param data: Список словарей с данными.
    :param start_row: Номер строки, с которой начнется добавление данных.
    """
    try:
        worksheet = table.worksheet(title)
    except exceptions.WorksheetNotFound:
        worksheet = create_worksheet(table, title, rows=100, cols=20)

    # Преобразуем список словарей в список списков для добавления через insert_rows
    headers = list(data[0].keys())
    rows = [[row[header] for header in headers] for row in data]

    print(rows)
    # Вставляем строки с данными в рабочий лист
    worksheet.insert_rows(rows, row=start_row)
    
def add_data_to_worksheet_var_2(table: Spreadsheet, title: str, data: List[Dict], start_row: int = 2) -> None:
    """
    Добовляет и обновляет данные на рабочем листе в Google Sheets.

    :param table: Объект таблицы (Spreadsheet).
    :param title: Название рабочего листа.
    :param data: Список словарей с данными.
    :param start_row: Номер строки, с которой начнется добавление данных.
    """
    try:
        worksheet = table.worksheet(title)
    except exceptions.WorksheetNotFound:
        worksheet = create_worksheet(table, title, rows=100, cols=20)

    headers = data[0].keys()
    end_row = start_row + len(data) - 1
    end_col = chr(ord('A') + len(headers) - 1)

    cell_range = f'A{start_row}:{end_col}{end_row}'
    cell_list = worksheet.range(cell_range)

    flat_data = []
    for row in data:
        for header in headers:
            flat_data.append(row[header])

    for i, cell in enumerate(cell_list):
        cell.value = flat_data[i]

    worksheet.update_cells(cell_list)

def test_get_data():
    """Тестирование извлечения данных из таблицы Google Sheets."""
    client = client_init_json()
    table = get_table_by_key(client, table_key)
    data = extract_data_from_sheet(table, 'Лист 1')
    for i in data:
        print(i)

def test_dell_data():
    """Тестирование удаления данных по указанному диапазону."""
    client = client_init_json()
    table = get_table_by_key(client, table_key)
    clear_range(table=table, sheet_name="Лист 1", start_cell="A10", end_cell="G11")

def test_dell_all_data():
    """Тестирование удаления данных по указанному диапазону."""
    client = client_init_json()
    table = get_table_by_key(client, table_key)
    clear_sheet(table=table, sheet_name="Лист 1")

if __name__ == '__main__':
    pass