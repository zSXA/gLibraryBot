from gspread import Client, Spreadsheet, service_account, exceptions
from typing import List, Dict


config_auth = 'glibrarybot-014a8a5f400f.json'
table_key = '1qPdi8-dwzekVP1vxE_7mRMtacn_LgcxjZHI_nvV7NMw'
client=service_account(filename=config_auth)
table=client.open_by_key(table_key)


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='glibrarybot-014a8a5f400f.json')

def get_table_by_key(client: Client, table_key):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_key)

def create_worksheet(table: Spreadsheet, title: str, rows: int, cols: int):
    """Создание листа в таблице."""
    return table.add_worksheet(title, rows, cols)

def get_data_from_sheet(table: Spreadsheet, sheet_main: str) -> List[Dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_main: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_main)
    headers = worksheet.row_values(7)  # Первая строка считается заголовками

    data = []
    rows = worksheet.get_all_values()[7:]  # Начинаем считывать с второй строки

    for row in rows:
       row_dict = {headers[i]: value for i, value in enumerate(row)}
       data.append(row_dict)
    return data

def update_data_to_sheet(table: Spreadsheet, title: str, data: List[Dict], start_row: int = 2) -> None:
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

def update_cell_to_sheet(table: Spreadsheet, title: str,
                        col: int, row: int, user):

    worksheet = table.worksheet(title)
    worksheet.update_cell(col, row, user)

def init_table(sheet_main: str, table_key=table_key):
    client=client_init_json()
    table=get_table_by_key(client, table_key)
    return get_data_from_sheet(table, sheet_main)

def get_data(sheet_main: str):
    data = init_table(sheet_main)
    return data

def get_books_2(sheet_main, user: str):
    data = get_data(sheet_main)
    books = []
    for item in data:
        book = item['Название книги']
        if item['Читатель'] != '':
            if item['Читатель'] == user:
                book = '📖' + book
            else:
                book = '📍' + book
        books.append(book)
    return books

def update_rent(user: str, book: str, sheet_main: str, row=-1):
    data = get_data()
    for item in data:
        if item['Название книги'] == book:
            row = data.index(item)
            break
    client=client_init_json()
    table=get_table_by_key(client, table_key)
    update_cell_to_sheet(table,sheet_main, 5, row+7,user)
    