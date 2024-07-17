import pandas as pd
import ai_trans
import sys
import re
import utility

# 名词库路径
p_translate_library = '名词库.xlsx'

# 相关信息列名称
sub_col = ['NodeObjectName','K2NodeName']

# 将输入文本中的英文单词提取出来，返回结果为数组
def parse(s):
    if not isinstance(s, str):
        return []
    e = re.findall(r'[a-zA-Z]+', s)
    return e


# 翻译名词库，这是从文件加载的
translate_library = dict()
# 翻译名词库，这是build时新增的
translate_library_new = dict()

file_load = ''

# 在翻译名词库查找结果，找不到结果时新增条目填入
def translate_with_library(m, s1='', s2=''):
    if m in translate_library:
        return translate_library[m]
    elif m in translate_library_new:
        return translate_library_new[m]
    else:
        print(f'{m}不存在于名词库，向AI查询翻译结果')
        t = ai_trans.translate(m, s1, s2)
        translate_library_new[m] = t
        return t

# 导出名词库
def translate_library_out(df):
    for k,v in translate_library_new.items():
        df.at[k, '翻译结果'] = v
        df.at[k, '是否新增'] = True

    df.to_excel(p_translate_library, index=True, index_label='待翻译')
    print(f'名词库更新完成，已输出结果到：'+p_translate_library)

# 导入名词库
def translate_library_read():
    try:
        df = pd.read_excel(p_translate_library, index_col='待翻译')
    except:
        return pd.DataFrame(columns=['翻译结果', '是否新增'])
    
    # 从DataFrame中加载字典
    for row in df.itertuples(index=True):
        translate_library[row.Index] = row.翻译结果

    print(f'已载入{len(translate_library)}条名词')
    return df

def build_library(df, df_lib):
    length = len(df)
    # for i in range(length):
    for row in df.itertuples(index=True):
        # l = parse(df.at[i,'待翻译'])
        l = parse(row.待翻译)
        out = dict()
        for _l in l:
            out[_l] = translate_with_library(_l, getattr(row, sub_col[0]), getattr(row, sub_col[1]))
        print(f"""[{row.Index}/{length}] {row.待翻译} => {out}""")
    translate_library_out(df_lib)

def translate_file(df,f):
    length = len(df)
    list_english = []
    if '翻译结果' not in df.columns:
        df['翻译结果'] = None
    for i in range(length):
        s = df.at[i,'待翻译']
        
        # 按字符串长度从长到短排序，以确保较长词会优先被替换
        translate_sorted_key = sorted(translate_library.keys(), key=len, reverse=True)

        if isinstance(s, str):
            # 遍历名词库进行翻译，以确保翻译结果完全与名词库一致
            for key in translate_sorted_key:
                try:
                    s = s.replace(key, translate_library[key])
                except:
                    print(f"""[{i}/{length}] {df.at[i,'待翻译']} ：异常，跳过""")

            # 移除空格
            try:
                s = s.replace(" ","")
            except:
                print(f"""[{i}/{length}] {df.at[i,'待翻译']} ：异常，跳过""")

            # 检查剩余英文，统计到list_englist
            matches = re.findall(r'[a-zA-Z]+', s)
            if len(matches) > 0:
                list_english.append(f"""[{i}/{length}] {df.at[i,'待翻译']} => {s}""")

        # 完成替换，写入替换结果
        df.at[i,'翻译结果'] = s
        print(f"""[{i}/{length}] {df.at[i,'待翻译']} => {df.at[i,'翻译结果']}""")
    # _f = utility.add_date_suffix(file_load)
    df.to_excel('translate_out.xlsx',sheet_name = '翻译页', index = False)
    
    if len(list_english) > 0:
        print(f'以下是依旧包含英文字符的翻译结果，请检查：')
        for l in list_english:
            print(l)

    print(f'翻译完成，已输出结果到translate_out.xlsx')

# 1. 翻译时去除空格
# 2. 目前词会被拆散解析，例如Drag and Drop，找个办法让名词库有带空格的组合词时查找替换时不会按Drag查找（按开头向后匹配？）
#

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

    file_load = args[1]
    df = utility.load_table(file_load)
    df_lib = translate_library_read()

    if build_mode:
        build_library(df, df_lib)
    if trans_mode:
        translate_file(df,file_load)
    if not build_mode and not trans_mode:
        print_usage()

# 程序入口
if __name__ == "__main__":
    main()