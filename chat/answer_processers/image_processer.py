import os
import re
import base64
from pathlib import Path
import streamlit as st

from chat.answer_processers.reference_processer import get_reference_list


def markdown_images(markdown):
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'

    return img_html


def markdown_insert_images(markdown, base_path):
    images = markdown_images(markdown)
    found_images = []  # 修改为一个列表，用于保存找到的图片信息
    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = os.path.join(base_path, image[2])

        if os.path.exists(image_path):
            found_images.append((image_markdown, image_alt, image_path))  # 将找到的图片信息添加到列表中

    return found_images  # 返回图片信息列表


def image_markdown(SOURCE, output):
    #reference_list = get_reference_list(result['input_documents'][:K])  <- #这个是map_reduce的方式
    reference_list= get_reference_list(SOURCE)
    image_reference = [(image_markdown, image_alt, image_path) for ref in reference_list for (image_markdown, image_alt, image_path) in markdown_insert_images(output, ref)]

    if image_reference:
        merged_markdown = output
        for image_markdown, image_alt, image_path in image_reference:
            img_html = img_to_html(image_path, image_alt)
            merged_markdown = merged_markdown.replace(image_markdown, img_html)

        st.markdown(merged_markdown, unsafe_allow_html=True)

        return True
    else:
        return False
    
