from gspread import Spreadsheet, service_account
from typing import List, Dict

class GoogleTable:

    def __init__(self, config_auth: str, table_key: str):
        self.client=service_account(filename=config_auth)
        self.table=self.client.open_by_key(table_key)
        self.data = []
    
    def __repr__(self) -> List[Dict]:
        return self.data

    def create_worksheet(self, title: str, rows: int, cols: int) -> Spreadsheet:
        """Создание листа в таблице."""
        return self.table.add_worksheet(title, rows, cols)
    
    def get_data_from_sheet(self, title: str, row: int) -> List[Dict]:
        """
        Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.
        """
        worksheet = self.table.worksheet(title)
        headers = worksheet.row_values(row)  # Первая строка считается заголовками

        rows = worksheet.get_all_values()[row:]  # Начинаем считывать со второй строки

        self.data.clear()
        for row in rows:
            row_dict = {headers[i]: value for i, value in enumerate(row)}
            self.data.append(row_dict)
        return self.data
    
    def update_cell_from_sheet(self, title: str, row: int, col: int, value):
        worksheet = self.table.worksheet(title)
        worksheet.update_cell(row, col, value)
        return 'Success'