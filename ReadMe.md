## 不变表

- 节点分类表.xlsx
- 名词库.xlsx

## 基本流程

- get_translate_content.py
    - 从DT导出的csv中提取节点分类及相关信息到out.xlsx
- excel_translate.py
    - —build
        - 从out.xlsx中建立名词库，同时进行AI初翻
    - 人工校对名词库
    - —trans
        - 使用名词库对out.xlsx进行翻译，结果输出到translate_out.xlsx
- action_override_process.py
    - —build
        - 从DT导出的csv中提取节点类型（NodeClassName），按函数、变量、事件等进行分类，导出结果到节点分类表.xlsx
        - —ai：由AI辅助分类
    - 根据节点分类表.xlsx与translate_out.xlsx，对DT导出的csv进行处理，输出final_out.csv
        - [x]  将一级分类分离
        - [ ]  构造本地化字符串key的时候加上前缀
    

## 更新流程

- 从编辑器导出增量表
- get_translate_content.py
    - 文件参数是增量表
    - 从增量表提取分类信息到out_增量.xlsx
- excel_translate.py
    - 文件参数是
    - —build
        - 从out_增量.xlsx追加名词库内容，AI初翻
    - 人工校对名词库
    - —trans
        - 使用名词库对out_增量.xlsx进行翻译，结果输出到translate_out_增量.xlsx
- action_override_process.py
    - 文件参数是增量表
    - —build
        - 从增量表提取节点类型
        - 加载节点分类表，将表里没有的节点类型加进去
            - [x]  增加加载已有节点分类表功能
    - 根据节点分类表，对增量表进行处理，将处理结果合并到原DT表
        - [x]  增加原表参数
        - [x]  增加对原表的加载
        - [x]  增加数据与原表的合并输出