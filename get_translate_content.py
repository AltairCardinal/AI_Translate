import pandas as pd
import sys
import utility

main_col = 'NodeCategory'
sub_col = ['NodeObjectName','K2NodeName']

def main():
    args = sys.argv
    if len(args) < 2:
        print("错误: 缺少文件名参数")

    # 加载表
    df = utility.load_table(args[1])
    print(df)

    # 获取主要列
    df_out = pd.DataFrame()
    mail_col_unique_list = df[main_col].unique().tolist()
    df_out['待翻译'] = mail_col_unique_list

    # 获取附属列
    for s in sub_col:
        df_out[s] = None
        for row in df_out.itertuples(index=True, name='待翻译'):
            r = df[df[main_col] == row.待翻译]
            df_out.at[row.Index, s] = r[s].unique().tolist()

    # 输出结果
    _f = utility.add_date_suffix('out.xlsx')
    df_out.to_excel(_f, sheet_name='翻译页', index = False)
    print(f'完成，已输出结果到{_f}')

# 程序入口
if __name__ == "__main__":
    main()