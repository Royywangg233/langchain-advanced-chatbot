# langchian-http-sources
can click sources to see the original documents in the chat channel


https://github.com/Royywangg233/langchian-http-sources/assets/133733744/ea701689-a6dd-48af-b9b1-a5713200def4

# 快速开始

## 准备

**1. 克隆项目代码：**

``` bash
git clone https://github.com/Royywangg233/langchian-http-sources.git
cd langchain-http-sources/
```

**2. 安装依赖：** \>

``` bash
pip3 install -r requirements.txt
```

**3. 用docsify使参考文档变成可点击的形式：**

``` bash
npm i docsify-cli -g
```

``` bash
docsify init ./docs #在docs目录下放入你的.md文件格式目录
```

``` bash
docsify serve docs
```
更多请参考[docsify](https://docsify.js.org/#/quickstart?id=initialize)


## 配置

配置`config.py` 文件：

``` bash
# openai config
API_O = "your-api-key" 指定你的API key

# setup
TEMPRETURE = 0.0
MODEL = 'gpt-3.5-turbo-16k-0613'
MESSAGE = False
K = 1
DEBUG = False #debug 参考文档准确性问题，初次运行不需要开启。

# index config
load_file_path = "/path/to/your/derictory" #指定要加载的目录路径 （目前只支持markdwon格式）
index_path = "/initialize/your/index/store/xxxxxxx.index" #指定要储存数据的向量库的路径
pkl_path = "/initialize/your/faiss/store/xxxxx.pkl" #指定构建faiss向量库的路径
```


## 运行

### 构建向量库

``` bash
python3 ingest.py
```

### 运行页面，开始聊天

``` bash
streamlit run main_1.py
```

