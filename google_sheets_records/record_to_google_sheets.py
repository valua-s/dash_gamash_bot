import gspread
from decouple import config


class TableDashaRecorder:

    def __init__(self):
        
        self.account = gspread.service_account(filename='service_account.json')
        self.spreadsheet = self.account.open_by_url('https://docs.google.com/spreadsheets/d/1oziWk80l7RD31H3SZDzeaqOKoaeHK7XxQ-j6RPHrkgs/edit?gid=0#gid=0')
        self.worksheet = self.spreadsheet.get_worksheet(0)
        self.names_of_columns: list = self.worksheet.row_values(1)

    def create_record(self, column, client_answer):
        row = self.next_available_row()
        self.worksheet.update_cell(int(row), int(column), f'{client_answer}')
    
    def next_available_row(self) -> int:
        str_list = list(filter(None, self.worksheet.col_values(1)))
        return len(str_list)+1

    def get_record_row_by_value(self, value):
        cell = self.worksheet.find(value)
        return cell.row

    def delete_record(self, value):
        try:
            row = self.get_record_row_by_value(value)
        except AttributeError:
            return 'Ты и не записался, друг мой'
        self.worksheet.batch_clear([f"A{row}:E{row}"])
        # for i in range(1, 6):
        #     self.worksheet.update_cell(int(row), i, '')
        return 'Успешное удаление'
    
    def get_all_records(self):
        items = []
        for row_num in self.worksheet.col_values(1):
            item = {}
            for col_num in range(1,5):
                item[self.worksheet.cell(row=1, col=col_num)]
        
    
    def create_assortiment_dict(self) -> [dict, int]:
        
        assortiment_dict: dict = {}
        names_of_column: [str] = self.worksheet.row_values(1)
    
        for name_of_column in names_of_column:
            cell = self.worksheet.find(name_of_column)
            values_list = self.worksheet.col_values(cell.col)[1:]
            assortiment_dict[name_of_column] = values_list
        
        return [assortiment_dict, len(values_list)]
    
    def create_all_records_list(self, start_from=2) -> list[dict]:
        
        result: list = []
        names_of_columns: list[str] = self.names_of_columns
        for row in range(start_from, self.next_available_row()):
            item: dict = {}
            
            for column in range(1, len(names_of_columns)):
                
                if names_of_columns[column] == 'amount':
                    item[names_of_columns[column]] = int(self.worksheet.cell(row=row, col=column+1).value)
                else:
                    item[names_of_columns[column]] = self.worksheet.cell(row=row, col=column+1).value
                
            result.append(item)
        return result

        