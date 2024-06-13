import pandas as pd
import ai_trans
import sys
import re

# 名词库路径
p_translate_library = '名词库.xlsx'

# 相关信息列名称
sub_col = ['NodeObjectName','K2NodeName']

# 将输入文本中的英文单词提取出来，返回结果为数组
def parse(s):
    e = re.findall(r'[a-zA-Z]+', s)
    return e


# 翻译名词库
translate_library = dict()

# 在翻译名词库查找结果，找不到结果时新增条目填入
def translate_with_library(m, s1, s2):
    if m in translate_library:
        return translate_library[m]
    else:
        t = ai_trans.translate(m, s1, s2)
        translate_library[m] = t
        return t

# 导出名词库
def translate_library_out():
    df = pd.DataFrame([translate_library])
    df.to_excel(p_translate_library, index=False)
    print(f'名词库更新完成，已输出结果到：'+p_translate_library)

# 导入名词库
def translate_library_read():
    try:
        df = pd.read_excel(p_translate_library)
    except:
        return
    return df.to_dict(orient='list')

def build_library(df):
    length = len(df)
    # for i in range(length):
    for row in df.itertuples(index=True):
        # l = parse(df.at[i,'待翻译'])
        l = parse(row.待翻译)
        out = dict()
        for _l in l:
            out[_l] = translate_with_library(_l, getattr(row, sub_col[0]), getattr(row, sub_col[1]))
        print(f"""[{row.Index}/{length}] {row.待翻译} => {out}""")
    translate_library_out()

def translate_file(df,f):
    length = len(df)
    if '翻译结果' not in df.columns:
        df['翻译结果'] = None
    for i in range(length):
        s = df.at[i,'待翻译']
        l = parse(s)
        for _l in l:
            s = s.replace(_l, translate_with_library(_l))
        df.at[i,'翻译结果'] = s
        print(f"""[{i}/{length}] {df.at[i,'待翻译']} => {df.at[i,'翻译结果']}""")
    df.to_excel('translate_out.xlsx',sheet_name = '翻译页', index = False)
    print(f'翻译完成，已输出结果到translate_out.xlsx')

def print_usage():
    usage = """
    用法:
        python excel_translate.py [文件名] [--build] [--trans]

    参数:
        文件名
            描述: 指定要处理的文件名。
            用法: 在命令行中直接提供文件名作为第一个参数。
            示例:
                python excel_translate.py example.xlsx

        --build
            描述: 建立名词库模式
            用法: 在命令行中使用 --build 参数。
            示例:
                python excel_translate.py example.xlsx --build

        --trans
            描述: 根据名词库进行翻译，输出结果到out_原始文件.xlsx
            用法: 在命令行中使用 --trans 参数。
            示例:
                python excel_translate.py example.xlsx --trans

    示例:
        仅指定文件名:
            python script.py example.txt

        建立名词库模式:
            python script.py example.txt --build

        进行翻译:
            python script.py example.txt --trans

        同时使用建立名词库模式和翻译:
            python script.py example.txt --build --trans
    """
    print(usage)

# 建立名词库
def main():
    args = sys.argv
    if len(args) < 2:
        print("错误: 缺少文件名参数")
        print_usage()
        sys.exit(1)
    build_mode = '--build' in sys.argv
    trans_mode = '--trans' in sys.argv


    df = pd.read_excel(args[1], sheet_name = '翻译页')
    translate_library_read()

    if build_mode:
        build_library(df)
    if trans_mode:
        translate_file(df,args[1])
    if not build_mode and not trans_mode:
        print_usage()

# 程序入口
if __name__ == "__main__":
    main()