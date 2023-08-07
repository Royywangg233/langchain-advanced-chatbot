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

## 配置

配置`config.py` 文件：

``` bash

```

**配置说明：**

**1.个人聊天**

-   个人聊天中，需要以 "[bot"或"\@bot](mailto:bot%22或%22@bot){.email}"
    为开头的内容触发机器人，对应配置项 `single_chat_prefix`
    (如果不需要以前缀触发可以填写 `"single_chat_prefix": [""]`)
-   机器人回复的内容会以 "[bot]" 作为前缀， 以区分真人，对应的配置项为
    `single_chat_reply_prefix` (如果不需要前缀可以填写
    `"single_chat_reply_prefix": ""`)

**2.群组聊天**

-   群组聊天中，群名称需配置在 `group_name_white_list`
    中才能开启群聊自动回复。如果想对所有群聊生效，可以直接填写
    `"group_name_white_list": ["ALL_GROUP"]`
-   默认只要被人 \@ 就会触发机器人自动回复；另外群聊天中只要检测到以
    "@bot" 开头的内容，同样会自动回复（方便自己触发），这对应配置项
    `group_chat_prefix`
-   可选配置:
    `group_name_keyword_white_list`配置项支持模糊匹配群名称，`group_chat_keyword`配置项则支持模糊匹配群消息内容，用法与上述两个配置项相同。（Contributed
    by [evolay](https://github.com/evolay))
-   `group_chat_in_one_session`：使群聊共享一个会话上下文，配置
    `["ALL_GROUP"]` 则作用于所有群聊

**3.语音识别**

-   添加 `"speech_recognition": true`
    将开启语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，该参数仅支持私聊
    (注意由于语音消息无法匹配前缀，一旦开启将对所有语音自动回复，支持语音触发画图)；
-   添加 `"group_speech_recognition": true`
    将开启群组语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，参数仅支持群聊
    (会匹配group_chat_prefix和group_chat_keyword, 支持语音触发画图)；
-   添加 `"voice_reply_voice": true`
    将开启语音回复语音（同时作用于私聊和群聊），但是需要配置对应语音合成平台的key，由于itchat协议的限制，只能发送语音mp3文件，若使用wechaty则回复的是微信语音。

**4.其他配置**

-   `model`: 模型名称，目前支持 `gpt-3.5-turbo`, `text-davinci-003`,
    `gpt-4`, `gpt-4-32k` (其中gpt-4 api暂未开放)
-   `temperature`,`frequency_penalty`,`presence_penalty`: Chat
    API接口参数，详情参考[OpenAI官方文档。](https://platform.openai.com/docs/api-reference/chat)
-   `proxy`：由于目前 `openai`
    接口国内无法访问，需配置代理客户端的地址，详情参考
    [#351](https://github.com/zhayujie/chatgpt-on-wechat/issues/351)
-   对于图像生成，在满足个人或群组触发条件外，还需要额外的关键词前缀来触发，对应配置
    `image_create_prefix`
-   关于OpenAI对话及图片接口的参数配置（内容自由度、回复字数限制、图片大小等），可以参考
    [对话接口](https://beta.openai.com/docs/api-reference/completions)
    和
    [图像接口](https://beta.openai.com/docs/api-reference/completions)
    文档直接在
    [代码](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/bot/openai/open_ai_bot.py)
    `bot/openai/open_ai_bot.py` 中进行调整。
-   `conversation_max_tokens`：表示能够记忆的上下文最大字数（一问一答为一组对话，如果累积的对话字数超出限制，就会优先移除最早的一组对话）
-   `rate_limit_chatgpt`，`rate_limit_dalle`：每分钟最高问答速率、画图速率，超速后排队按序处理。
-   `clear_memory_commands`:
    对话内指令，主动清空前文记忆，字符串数组可自定义指令别名。
-   `hot_reload`: 程序退出后，暂存微信扫码状态，默认关闭。
-   `character_desc`
    配置中保存着你对机器人说的一段话，他会记住这段话并作为他的设定，你可以为他定制任何人格
    (关于会话上下文的更多内容参考该
    [issue](https://github.com/zhayujie/chatgpt-on-wechat/issues/43))
-   `subscribe_msg`：订阅消息，公众号和企业微信channel中请填写，当被订阅时会自动回复，
    可使用特殊占位符。目前支持的占位符有{trigger_prefix}，在程序中它会自动替换成bot的触发词。

**所有可选的配置项均在该[文件](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py)中列出。**

## 运行

### 1.本地运行

如果是开发机 **本地运行**，直接在项目根目录下执行：

``` bash
python3 app.py
```

终端输出二维码后，使用微信进行扫码，当输出 "Start auto replying"
时表示自动回复程序已经成功运行了（注意：用于登录的微信需要在支付处已完成实名认证）。扫码登录后你的账号就成为机器人了，可以在微信手机端通过配置的关键词触发自动回复
(任意好友发送消息给你，或是自己发消息给好友)，参考[#142](https://github.com/zhayujie/chatgpt-on-wechat/issues/142)。

