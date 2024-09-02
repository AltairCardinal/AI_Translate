import sqlite3
import polib
import os
import sys
import glob
from tqdm import tqdm

'''
用法：
1. 初次使用时从脚本所在目录的子目录po中加载数据库，无数据库时从.po文件构建
2. 通过get_translate(key)方法获取给定key对应的翻译的集
'''

# 配置
_PO_DIR = 'po'
_DB = 'po.db'

# 加载目录下所有.po文件，key为po_entries[x].msgid，text为po_entries[x].msgstr
def load_all_po(_dir):
    # 遍历目录下的.po文件
    po_files = glob.glob(os.path.join(_dir, '*.po'))
    # # 目录下所有.po文件中的条目列表
    # po_entries = []
    # for _p in po_files:
    #     po_entries.append(polib.pofile(_p))
    return po_files

# 创建数据库表，返回连接对象
def create_db(_dir):
    conn = sqlite3.connect(os.path.join(_dir, _DB))
    # 创建一个游标对象
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS po_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        msgid TEXT,
        context TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_entry_id INTEGER,
        msgstr TEXT,
        FOREIGN KEY (po_entry_id) REFERENCES po_entries(id)
    )
    ''')
    # 创建索引以优化查重速度
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_po_entries ON po_entries (file_name, msgid, context)
    ''')
    
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_translations ON translations (po_entry_id, msgstr)
    ''')
    conn.commit()
    return conn

# 从po文件从头构建数据库
def build_po_new(_c, _file_path):
    po = polib.pofile(_file_path)
    file_name = _file_path.split('\\')[-1]
    c = _c.cursor()
    
    for entry in tqdm(po, desc=f'正在处理{file_name}'):
        # 检查 po_entries 表中是否已经存在相同的记录
        c.execute('''
        SELECT id FROM po_entries WHERE file_name = ? AND msgid = ? AND context = ?
        ''', (file_name, entry.msgid, entry.msgctxt))
        
        po_entry = c.fetchone()
        
        if po_entry is None:
            # 插入 po_entries 表
            c.execute('''
            INSERT INTO po_entries (file_name, msgid, context)
            VALUES (?, ?, ?)
            ''', (file_name, entry.msgid, entry.msgctxt))
        
            po_entry_id = c.lastrowid
        else:
            po_entry_id = po_entry[0]
        
        # 插入 translations 表
        for msgstr in entry.msgstr.split('\n'):
            # 检查 translations 表中是否已经存在相同的记录
            c.execute('''
            SELECT id FROM translations WHERE po_entry_id = ? AND msgstr = ?
            ''', (po_entry_id, msgstr))
            
            translation = c.fetchone()
            
            if translation is None:
                c.execute('''
                INSERT INTO translations (po_entry_id, msgstr)
                VALUES (?, ?)
                ''', (po_entry_id, msgstr))
    _c.commit()
    print(f'已加载本地化文件：{file_name}')

def load_db(_dir):
    db_path = os.path.join(_dir, _DB)
    # 检查数据库是否存在，不存在则从po重新创建
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
    else:
        construct_db(_dir)
    return conn

def construct_db(_dir):
    # 加载所有po文件
    po_files = load_all_po(_dir)
    # 重新创建数据库表
    conn = create_db(_dir)
    # 重新加载所有po文件到数据库表
    for _f in po_files:
        build_po_new(conn, _f)
    return conn

# 查询翻译
def get_translations_ori(_c, _msgid):
    _c.execute('''
    SELECT po_entries.file_name, po_entries.msgid, po_entries.context, translations.msgstr
    FROM po_entries
    JOIN translations ON po_entries.id = translations.po_entry_id
    WHERE po_entries.msgid = ?
    ''', (_msgid,))
    
    results = _c.fetchall()
    
    translations_list = []
    for row in results:
        translations_list.append({
            'file_name': row[0],
            'msgid': row[1],
            'context': row[2],
            'msgstr': row[3]
        })
    
    return translations_list

def get_translations(_msgid, _c = None):
    if _c == None:
        load_db(po_dir)

    r = get_translations_ori(_c, _msgid)
    rr = set()
    for _r in r:
        if _r != '':
            rr.add(_r['msgstr'])
    return rr

# # 查询数据
# def try_get_po(_c, _key):
#     _c.execute('SELECT * FROM po WHERE key =' + _key + ';')
#     rows = _c.fetchall()
#     for row in rows:
#         print(row)

# 关闭连接
def close_db(_c):
    _c.close()

# 子目录处理
script_dir = os.path.dirname(os.path.abspath(__file__))
po_dir = os.path.join(script_dir, _PO_DIR)
if not os.path.isdir(po_dir):    
    print('找不到po子目录，请在脚本所在目录新建文件夹po，并放入所有.po文件')

# 建立名词库
def main():
    # 运行参数响应
    args = sys.argv
    build_phase = '--build' in args
    debug_mode = '--debug' in args
    debug_mode = True


    if build_phase:
        # 从po文件构建数据库
        c = construct_db(po_dir)
    else:
        # 加载现有po数据库
        c = load_db(po_dir)

    # 调试用，手动查询数据库条目
    while debug_mode:
        user_input = input('输入要查询的本地化条目id：')
        result = get_translations(user_input, c.cursor())
        print('查询结果如下：')
        print(result)
    

# 程序入口
if __name__ == "__main__":
    main()

