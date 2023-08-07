import urllib.parse
import os

from config import load_file_path

def get_reference_list(SOURCE):
    return [os.path.dirname(SOURCE)]


def replace_with_http_link(match):
    base_url = "http://localhost:3000/#/"
    path = match.group(0)
    
    # 找到最后一个斜杠的索引
    last_slash_index = load_file_path.rfind('/')
    
    # 提取包含最后一个斜杠之前的部分
    extracted_part = load_file_path[:last_slash_index + 1]
    path = path.replace(extracted_part, "")
    
    # 移除 ".md" 部分
    path = path.replace(".md", "")
    
    # 使用 urllib.parse.quote 对路径进行 URL 编码
    encoded_path = urllib.parse.quote(path)
    
    return f'<a href="{base_url}{encoded_path}">{path}.md</a>'


def reference_pattern():
    pattern = fr"{load_file_path}/.*\.md"
    return pattern
