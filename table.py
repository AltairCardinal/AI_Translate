import re
import pandas as pd

markdown_list = """
    - AreaID:通过Trigger Box发送事件，给Trigger Box赋予ID
	- Trigger Type:进入/离开
	- Trigger Actor Type:玩家角色/非玩家角色/角色/任意
	- Camp Set:阵营A~H/MAX
"""

# 使用正则表达式解析列表
pattern = re.compile(r'-\s*(.*?):(.*)')
matches = pattern.findall(markdown_list)

# 将解析结果转换为字典
data = {match[0].strip(): match[1].strip() for match in matches}

# 将字典转换为DataFrame
df = pd.DataFrame(list(data.items()), columns=['Field', 'Description'])

# 将DataFrame转换为Markdown表格
markdown_table = df.to_markdown(index=False)

print(markdown_table)