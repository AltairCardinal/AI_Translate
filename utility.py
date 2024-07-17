import pandas as pd
from pathlib import Path
import chardet
from datetime import datetime

# 文件编码检测
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# 多格式加载表格为DataFrame
def load_table(f):
    path = Path(f)
    file_extension = path.suffix

    if file_extension == '.csv':
        return pd.read_csv(f, encoding=detect_encoding(f))
    elif file_extension in ['.xls', '.xlsx']:
        return pd.read_excel(f)
    else:
        raise ValueError(f'不支持的文件类型：{file_extension}')

# 为文件路径中的文件名添加后缀
def add_suffix(f, suffix):
    path = Path(f)
    return path.with_name(f'{path.stem}{suffix}{path.suffix}')

# 获取格式化日期与时间
def get_format_datetime():
    return datetime.now().strftime('%m%d%H%M')

# 为文件路径中的文件名添加以日期+时间组成的后缀
def add_date_suffix(f):
    return add_suffix(f, '_'+get_format_datetime())