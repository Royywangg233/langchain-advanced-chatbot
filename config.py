# openai config
API_O = "your-api-key"


# setup
TEMPRETURE = 0.0
MODEL = 'gpt-3.5-turbo-16k-0613'
MESSAGE = False
K = 1
DEBUG = False


# index config
load_file_path = "/path/to/your/derictory" #指定要加载的目录路径下的所有markdown格式文件
index_path = "/initialize/your/index/store/xxxxxxx.index" #指定要储存数据的向量库的路径
pkl_path = "/initialize/your/faiss/store/xxxxx.pkl" #指定构建faiss向量库的路径