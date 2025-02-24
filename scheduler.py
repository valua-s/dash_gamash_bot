import asyncio


from google_sheets_records.record_to_google_sheets import TableDashaRecorder
from db_handler.db_info import DB


async def get_from_worksheet_append_to_db():

    recorder = TableDashaRecorder()
    db = DB()
    # import pdb; pdb.set_trace()
    records_in_table = await db.get_records_count()
    if recorder.next_available_row()-1 > records_in_table:

        worksheet_data = recorder.create_all_records_list(
            start_from=records_in_table + 2
            )
        await db.create(data=worksheet_data)

asyncio.run(get_from_worksheet_append_to_db())
