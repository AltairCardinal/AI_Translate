"""
用来处理DT_BlueprintActionsOverrideConfig表




"""

import pandas as pd
import sys
import chardet
import ai
from string import Template
import utility



NodeClassName = 'NodeClassName'
NodeCategory = 'NodeCategory'
OverrideCategory = 'OverrideCategory'
IsOverrideSource = 'IsOverrideSource'
NewOverrideCategory_Name = 'NewOverrideCategory_Name'
NodeCatagory_in_library = '分类'
filename_NodeClassName_library = '节点分类表.xlsx'
filename_translate_library = 'translate_out.xlsx'
loc_space = 'DT_BlueprintActionsOverrideConfig [311CDFF94BDC825A10BD37A0F1CE17E0]'
loc_key_prefix = 'CategoryOverride_'
loc_form = Template("""NSLOCTEXT("$SPACE", "$KEY", "$TEXT")""")

dict_loc_key = dict()
encoding = ''

prompt = Template("""
    UE中$N属于什么分类？从可选项中选一个回答。回答内容除了可选项外不要有任何其他内容。
    可选项有：
    函数
    变量
    事件
    流程控制
    数学
    类型转换
    其他
    """
)

main_category_dict={
    '变量': 'Variable',
    '函数': 'Function',
    '流程控制': 'Flow',
    '事件': 'Event',
    '类型转换': 'Cast',
    '数学': 'Math',
    '其他': "Other",
    '工具': 'Utility'
}

# 更新并导出节点分类表
def update_NodeClassName_library(df, is_ai=False):
    l = df[NodeClassName].unique().tolist()
    df_lib = get_NodeClassName_library(filename_NodeClassName_library)

    new_items = [item for item in l if item not in df_lib.index.tolist()]
    if new_items:
        for i, v in enumerate(new_items):
            df_lib.at[v, NodeCatagory_in_library] = ai.ask_ai(prompt.substitute(N=v)) if is_ai else ''
            print(f"""[{i+1}/{len(new_items)}] {v} ： {df_lib.at[v, NodeCatagory_in_library]}""")   
    df_lib.to_excel(filename_NodeClassName_library, index=True, index_label=NodeClassName)

# 尝试从文件加载节点分类表
def get_NodeClassName_library(f):
    try:
        df = pd.read_excel(f, index_col=NodeClassName)
    except:
        return pd.DataFrame(columns=[NodeCategory])
    return df

# 获取本地化字符串
def get_localtrans_str(key,text):
    return loc_form.substitute(SPACE=loc_space, KEY=key, TEXT=text)

def remove_prefix(s):
    for i in main_category_dict.keys():
        if s.startswith(i):
            s = s[len(i)+1:]
            return str(s)
    return str(s)

# 构建覆写节点分类内容
def to_catagory(df, ori_file_path = ''):
    # 加载节点类型分类表
    df_nodeclass_lib = get_NodeClassName_library(filename_NodeClassName_library)
    # 加载翻译表
    df_trans_lib = pd.read_excel(filename_translate_library, index_col='待翻译')
    # 确保原表数据类型正确
    df[OverrideCategory] = df[OverrideCategory].astype(str)
    df[IsOverrideSource] = df[IsOverrideSource].astype(bool)
    df[NewOverrideCategory_Name] = df[NewOverrideCategory_Name].astype(str)

    for row in df.itertuples(index=True):
        nodeclass_catagory = main_category_dict[str(df_nodeclass_lib.at[getattr(row, NodeClassName), NodeCatagory_in_library])]
        trans_catagory = str(df_trans_lib.at[getattr(row, NodeCategory),'翻译结果'])
        total_catagory = remove_prefix(trans_catagory)
        # 构建本地化字符串
        loc_catagory = get_localtrans_str(getattr(row, NodeCategory), total_catagory)
        df.at[row.Index,OverrideCategory] = loc_catagory
        df.at[row.Index,IsOverrideSource] = True
        df.at[row.Index,NewOverrideCategory_Name] = nodeclass_catagory
    
    catagory_icon_name = df[NewOverrideCategory_Name].unique().tolist()
    print(f'以下为用于图标配置的一级分类fname：')
    for l in catagory_icon_name:
        print(l)
    

    if ori_file_path == '':
        print(f'处理原文件')
        df.to_csv('final_out2.csv', encoding='utf-8-sig', index=False, sep=',')
    else:
        ori_df = utility.load_table(ori_file_path)
        # max_index_ori_df = ori_df.index.max() + 1
        # df.index = range(max_index_ori_df, max_index_ori_df + len(df))
        df_out = pd.concat([ori_df, df], axis=0)
        df_out = df_out.reset_index(drop=True)
        df_out['---'] = df_out.index
        df_out.to_csv('final_out3.csv', encoding='utf-8-sig', index=False, sep=',')


# 主函数
def main():
    args = sys.argv
    if len(args) < 2:
        print("错误: 缺少文件名参数")
        sys.exit(1)
    build_mode = '--build' in sys.argv
    is_ai = '--ai' in sys.argv

    file_path = args[1]
    ori_file_path = args[2] if len(args) > 2 and args[2].endswith('.csv') else ''

    df = utility.load_table(file_path)

    if build_mode:
        update_NodeClassName_library(df,is_ai)
    else:
        to_catagory(df,ori_file_path)



# 程序入口
if __name__ == "__main__":
    main()