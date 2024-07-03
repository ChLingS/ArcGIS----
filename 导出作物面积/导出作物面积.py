import pandas as pd
from asset.Global import DataRead


class ExportFlamlandExcel:
    def __init__(self, table_path: str, save_path: str):
        self.table = DataRead(table_path)
        self.save = save_path

    def create_index_fied(self):
        self.table['index_fied'] = self.table['cun'].astype(str) + self.table['xian'].astype(str)

    def get_cun_unique(self) -> list[str]:
        return self.table['index_fied'].unique().tolist()

    def create_area_table(self):
        self.create_index_fied()
        unique = self.get_cun_unique()
        new_df = pd.DataFrame(columns=['sheng', 'sheng_code',
                                       'shi', 'shi_code',
                                       'xian', 'xian_code',
                                       'zhen', 'zhen_code',
                                       'cun', 'cun_code',
                                       '面积（亩）'])
        for index_field in unique:
            df = self.table[(self.table['index_fied'] == index_field)]
            area_sum = sum(df["mianji"].to_list())
            df_frist = df.iloc[0]
            new_row: dict = {
                'sheng': df_frist['sheng'],
                'sheng_code': df_frist['sheng_code'],
                'shi': df_frist['shi'],
                'shi_code': df_frist['shi_code'],
                'xian': df_frist['xian'],
                'xian_code': df_frist['xian_code'],
                'zhen': df_frist['zhen'],
                'zhen_code': df_frist['zhen_code'],
                'cun': df_frist['cun'],
                'cun_code': df_frist['cun_code'],
                '面积（亩）': area_sum/666.67}
            new_df.loc[len(new_df)] = new_row
        print(self.save)
        new_df.to_excel(self.save, index_label=False)



if __name__ == "__main__":
    table = ExportFlamlandExcel("F:\测试\out\江西省抚州市.shp", "F:\测试\out\江西省抚州市.xlsx")
    table.create_area_table()
