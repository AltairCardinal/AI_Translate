import pandas as pd
import sys

main_col = 'NodeCategory'
sub_col = ['NodeObjectName','K2NodeName']

def main():
    args = sys.argv
    if len(args) < 2:
        print("错误: 缺少文件名参数")

    # 加载表
    df = pd.read_excel(args[1])

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
    df_out.to_excel('out.xlsx', sheet_name='翻译页', index = False)
    print(f'完成，已输出结果到out.xlsx')

# 程序入口
if __name__ == "__main__":
    main()