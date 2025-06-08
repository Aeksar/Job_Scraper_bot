import pandas as pd
import io


def to_exel(data: dict):
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    excel_file.seek(0)
    return excel_file.read()