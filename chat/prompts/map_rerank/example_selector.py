from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

import os
import openai

from config import API_0

os.environ["OPENAI_API_KEY"] = API_0


examples = [
  {
    "question": "悟空能不能获取AppKey?",
    "context": 
"""
context:
2、如何获取AppKey？<br />（1）进入听云-悟空，点击App，进入如下页面![image.png](./assets/1636094408321-c144565f-cd3c-401a-9bd7-023572f88224.png)
（2）点击添加应用![image.png](./assets/1636094408206-a8e22d57-baff-4fdd-b5ce-2d58ca5572be.png)
（3）选择选项，得到AppKey![image.png](./assets/1636094408900-80bf801b-327b-47a0-b95e-c33148a064a2.png)
Helpful Answer: 能。
Score: 90
"""
  },
  {
    "question": "k100s单机环境搭建时，容器可不可以使用Containerd",
    "context": 
"""
k3s单机环境搭建，容器使用默认Containerd
Helpful Answer: 不可以。
Score: 90
"""
  },
  {
    "question": "k3s单机环境搭建时，容器可不可以使用Containerd",
    "context": 
"""
k3s单机环境搭建，容器使用默认Containerd
Helpful Answer: 可以。
Score: 90
"""
  },
  {
    "question": "IOS嵌码的步骤",
    "context": 
"""
**3、 了解了Xcode通用知识后，我们开始进行IOS嵌码**<br />**3.1我们以saas3.0为示例做嵌码。我们先从微盘上或者找同事要到3.0sdk的压缩包。把压缩包放到桌面上，解压sdk为2.15.9.zip**<br />![image.gif](./assets/1650795905598-e83ff0f0-f39f-4b70-9698-3486db93e50f.gif)
**3.2我们在解压的文件夹中找到IOS部署文档，然后打开嵌码帮助文档**<br />![image.gif](./assets/1650796028539-92a4634f-8b51-4f96-b05e-7d1353dc7fff.gif)
**3.3我们使用手动集成听云sdk。所以可以忽略Cocoapods，直接看到手动集成。**<br />**将tingyunApp.framework拖拽到项目中。按照帮助文档，把该勾选的勾选上！**<br />![image.gif](./assets/1650796061875-db8acb67-693d-45b2-9419-66b1c4836c96.gif)
**3.4这个时候，在Liucj项目中，就有了tingyunApp.Framework。我们再看帮助文档中的1.2**<br />![image.gif](./assets/1650796315684-7d349fa8-8239-47e2-a6a1-b862febd97cb.gif)
设置完-ObjC，我们找到Build Setting旁边的Build Phases。按照文档添加依赖库(帮助文档上写的依赖库最好全加上)
![image.gif](./assets/1650796339756-09e66dc2-f086-41f5-9a5e-4565561db874.gif)
**3.5这个时候项目Liucj中就会有个Frameworks，这个文件底下全是你添加的依赖包。在Liucj主项目文件夹中找到main.m文件并添加#import <tingyun/NBSAppAgent.h>(添加NBSAppAgent.framework库的时候，要按照3.3的流程步骤，放对位置)**<br />**注意*(如果没按照3.3的说明，把framework库放到了别的位置，就要修改路径，按照你放库的路径进行修改。例如：<tingyun/App/NBSAppAgent.h>)**<br />(main.m是入口函数，所有程序都由此进入)
![image.gif](./assets/1650796427798-a5665442-a419-4362-ae56-5e1eb5c38e3a.gif)
**3.6我们按照文档初始化SDK。先在平台上找到App模块，进入应用列表，在右上角添加应用**<br />![image.gif](./assets/1650796490455-1ffd0a03-b495-4909-8bef-38ddb37ed2ef.gif)
![image.gif](./assets/1650796539354-1af526e8-6473-485a-9298-72667087936f.gif)
![image.gif](./assets/1650796575236-d90a0735-0b83-46e0-acfb-50199b8270ca.gif)
(这时候会生成App Key和host，host是上传的地址，App Key是区别应用的标识)
**3.7我们在项目中main.m把文档上Objective-C的初始化代码放到自己的项目中。代码里的App key要和host一一对应填入**<br />![image.gif](./assets/1650796587791-2ef1dfd0-3a25-4682-8a41-6c4ccdb33c4e.gif)
**3.8完成前面7步之后，嵌码就完成了。我们把测试手机和电脑连接上，在红框位置，选择你连接电脑的手机。**<br />![image.gif](./assets/1650796666783-cf4bc951-9634-4119-8a5e-acb5113dde22.gif)
![image.gif](./assets/1650796673356-c4349f77-9278-4f63-af34-6b76a415e893.gif)
确认选择手机无误后，我们在上方选择栏中找到Project，并且选择第一个选项Run：<br />![image.gif](./assets/1650796680204-8344869a-83a2-4e28-9936-fdc47fbc54a4.gif)
这个时候需要你当时设置Team时的密码(这块儿输入有可能是你设置Team的密码，也有可能是你电脑的屏保密码。可以尝试一下，看看哪个密码正确)
**3.9 Run一遍之后，不会报错，并且显示Build Success的提示，那你创建项目就成功了。这个时候，你连接的手机上就会出现一个空白的应用**<br />![image.gif](./assets/1650796719918-2682c505-0f32-464c-b7b8-cef149b988fd.gif)
我们现在需要到手机上的：设置-通用-描述文件与设备管理中找到你刚刚安装上的项目。点击进去，选择信任。<br />![image.gif](./assets/1650796745141-dcc411e9-f5f9-481d-b2f1-e5e1db63dff0.gif)
**3.10 我们先在Xcode里打开log日志，command+shift+y。再选择Project，再run一遍项目。连接的手机会自动弹出应用，并且会在log里打出嵌码日志。**<br />![image.gif](./assets/1650796772466-db2dc961-0e5d-434b-b5b5-b475cc98530d.gif)
![image.gif](./assets/1650796796282-c2c6c9dd-f6ee-41e1-9988-e4c2f5ebcae0.gif)
**只有出现Success to connect to NBSSERVER，才代表嵌码成功。**<br />我们再去平台上找到对应创建的应用。发现平台上有数据，IOS sdk嵌码成功。<br />![image.gif](./assets/1650796815851-6d8d204a-3577-403b-a50b-5343912c3db2.gif)
Helpful Answer: - 3.1 从微盘上或者同事那里获取3.0sdk的压缩包，并解压为2.15.9.zip
\n- 3.2 打开解压后的文件夹中的IOS部署文档，查看嵌码帮助文档
\n- 3.3 手动集成听云sdk，将tingyunApp.framework拖拽到项目中，并按照文档中的要求进行设置
\n- 3.4 在项目中找到main.m文件，并添加#import <tingyun/NBSAppAgent.h>，注意路径要正确
\n- 3.5 在Build Phases中添加依赖库，按照文档中的要求添加
\n- 3.6 在平台上创建应用，并获取App Key和host
\n- 3.7 在项目的main.m文件中初始化SDK，将App Key和host填入代码中
\n- 3.8 连接测试手机，选择手机并点击Run进行运行
\n- 3.9 在手机的设置中信任刚刚安装的应用
\n- 3.10 在Xcode中打开log日志，再次运行项目，确保嵌码成功"
Score: 100
"""
  },
  {
    "question": "IOS嵌码的详细步骤",
    "context": 
"""
**3、 了解了Xcode通用知识后，我们开始进行IOS嵌码**<br />**3.1我们以saas3.0为示例做嵌码。我们先从微盘上或者找同事要到3.0sdk的压缩包。把压缩包放到桌面上，解压sdk为2.15.9.zip**<br />![image.gif](./assets/1650795905598-e83ff0f0-f39f-4b70-9698-3486db93e50f.gif)
**3.2我们在解压的文件夹中找到IOS部署文档，然后打开嵌码帮助文档**<br />![image.gif](./assets/1650796028539-92a4634f-8b51-4f96-b05e-7d1353dc7fff.gif)
**3.3我们使用手动集成听云sdk。所以可以忽略Cocoapods，直接看到手动集成。**<br />**将tingyunApp.framework拖拽到项目中。按照帮助文档，把该勾选的勾选上！**<br />![image.gif](./assets/1650796061875-db8acb67-693d-45b2-9419-66b1c4836c96.gif)
**3.4这个时候，在Liucj项目中，就有了tingyunApp.Framework。我们再看帮助文档中的1.2**<br />![image.gif](./assets/1650796315684-7d349fa8-8239-47e2-a6a1-b862febd97cb.gif)
设置完-ObjC，我们找到Build Setting旁边的Build Phases。按照文档添加依赖库(帮助文档上写的依赖库最好全加上)
![image.gif](./assets/1650796339756-09e66dc2-f086-41f5-9a5e-4565561db874.gif)
**3.5这个时候项目Liucj中就会有个Frameworks，这个文件底下全是你添加的依赖包。在Liucj主项目文件夹中找到main.m文件并添加#import <tingyun/NBSAppAgent.h>(添加NBSAppAgent.framework库的时候，要按照3.3的流程步骤，放对位置)**<br />**注意*(如果没按照3.3的说明，把framework库放到了别的位置，就要修改路径，按照你放库的路径进行修改。例如：<tingyun/App/NBSAppAgent.h>)**<br />(main.m是入口函数，所有程序都由此进入)
![image.gif](./assets/1650796427798-a5665442-a419-4362-ae56-5e1eb5c38e3a.gif)
**3.6我们按照文档初始化SDK。先在平台上找到App模块，进入应用列表，在右上角添加应用**<br />![image.gif](./assets/1650796490455-1ffd0a03-b495-4909-8bef-38ddb37ed2ef.gif)
![image.gif](./assets/1650796539354-1af526e8-6473-485a-9298-72667087936f.gif)
![image.gif](./assets/1650796575236-d90a0735-0b83-46e0-acfb-50199b8270ca.gif)
(这时候会生成App Key和host，host是上传的地址，App Key是区别应用的标识)
**3.7我们在项目中main.m把文档上Objective-C的初始化代码放到自己的项目中。代码里的App key要和host一一对应填入**<br />![image.gif](./assets/1650796587791-2ef1dfd0-3a25-4682-8a41-6c4ccdb33c4e.gif)
**3.8完成前面7步之后，嵌码就完成了。我们把测试手机和电脑连接上，在红框位置，选择你连接电脑的手机。**<br />![image.gif](./assets/1650796666783-cf4bc951-9634-4119-8a5e-acb5113dde22.gif)
![image.gif](./assets/1650796673356-c4349f77-9278-4f63-af34-6b76a415e893.gif)
确认选择手机无误后，我们在上方选择栏中找到Project，并且选择第一个选项Run：<br />![image.gif](./assets/1650796680204-8344869a-83a2-4e28-9936-fdc47fbc54a4.gif)
这个时候需要你当时设置Team时的密码(这块儿输入有可能是你设置Team的密码，也有可能是你电脑的屏保密码。可以尝试一下，看看哪个密码正确)
**3.9 Run一遍之后，不会报错，并且显示Build Success的提示，那你创建项目就成功了。这个时候，你连接的手机上就会出现一个空白的应用**<br />![image.gif](./assets/1650796719918-2682c505-0f32-464c-b7b8-cef149b988fd.gif)
我们现在需要到手机上的：设置-通用-描述文件与设备管理中找到你刚刚安装上的项目。点击进去，选择信任。<br />![image.gif](./assets/1650796745141-dcc411e9-f5f9-481d-b2f1-e5e1db63dff0.gif)
**3.10 我们先在Xcode里打开log日志，command+shift+y。再选择Project，再run一遍项目。连接的手机会自动弹出应用，并且会在log里打出嵌码日志。**<br />![image.gif](./assets/1650796772466-db2dc961-0e5d-434b-b5b5-b475cc98530d.gif)
![image.gif](./assets/1650796796282-c2c6c9dd-f6ee-41e1-9988-e4c2f5ebcae0.gif)
**只有出现Success to connect to NBSSERVER，才代表嵌码成功。**<br />我们再去平台上找到对应创建的应用。发现平台上有数据，IOS sdk嵌码成功。<br />![image.gif](./assets/1650796815851-6d8d204a-3577-403b-a50b-5343912c3db2.gif) 
Helpful Answer: **3、 了解了Xcode通用知识后，我们开始进行IOS嵌码**<br />**3.1我们以saas3.0为示例做嵌码。我们先从微盘上或者找同事要到3.0sdk的压缩包。把压缩包放到桌面上，解压sdk为2.15.9.zip**<br />![image.gif](./assets/1650795905598-e83ff0f0-f39f-4b70-9698-3486db93e50f.gif)
**3.2我们在解压的文件夹中找到IOS部署文档，然后打开嵌码帮助文档**<br />![image.gif](./assets/1650796028539-92a4634f-8b51-4f96-b05e-7d1353dc7fff.gif)
**3.3我们使用手动集成听云sdk。所以可以忽略Cocoapods，直接看到手动集成。**<br />**将tingyunApp.framework拖拽到项目中。按照帮助文档，把该勾选的勾选上！**<br />![image.gif](./assets/1650796061875-db8acb67-693d-45b2-9419-66b1c4836c96.gif)
**3.4这个时候，在Liucj项目中，就有了tingyunApp.Framework。我们再看帮助文档中的1.2**<br />![image.gif](./assets/1650796315684-7d349fa8-8239-47e2-a6a1-b862febd97cb.gif)
设置完-ObjC，我们找到Build Setting旁边的Build Phases。按照文档添加依赖库(帮助文档上写的依赖库最好全加上)
![image.gif](./assets/1650796339756-09e66dc2-f086-41f5-9a5e-4565561db874.gif)
**3.5这个时候项目Liucj中就会有个Frameworks，这个文件底下全是你添加的依赖包。在Liucj主项目文件夹中找到main.m文件并添加#import <tingyun/NBSAppAgent.h>(添加NBSAppAgent.framework库的时候，要按照3.3的流程步骤，放对位置)**<br />**注意*(如果没按照3.3的说明，把framework库放到了别的位置，就要修改路径，按照你放库的路径进行修改。例如：<tingyun/App/NBSAppAgent.h>)**<br />(main.m是入口函数，所有程序都由此进入)
![image.gif](./assets/1650796427798-a5665442-a419-4362-ae56-5e1eb5c38e3a.gif)
**3.6我们按照文档初始化SDK。先在平台上找到App模块，进入应用列表，在右上角添加应用**<br />![image.gif](./assets/1650796490455-1ffd0a03-b495-4909-8bef-38ddb37ed2ef.gif)
![image.gif](./assets/1650796539354-1af526e8-6473-485a-9298-72667087936f.gif)
![image.gif](./assets/1650796575236-d90a0735-0b83-46e0-acfb-50199b8270ca.gif)
(这时候会生成App Key和host，host是上传的地址，App Key是区别应用的标识)
**3.7我们在项目中main.m把文档上Objective-C的初始化代码放到自己的项目中。代码里的App key要和host一一对应填入**<br />![image.gif](./assets/1650796587791-2ef1dfd0-3a25-4682-8a41-6c4ccdb33c4e.gif)
**3.8完成前面7步之后，嵌码就完成了。我们把测试手机和电脑连接上，在红框位置，选择你连接电脑的手机。**<br />![image.gif](./assets/1650796666783-cf4bc951-9634-4119-8a5e-acb5113dde22.gif)
![image.gif](./assets/1650796673356-c4349f77-9278-4f63-af34-6b76a415e893.gif)
确认选择手机无误后，我们在上方选择栏中找到Project，并且选择第一个选项Run：<br />![image.gif](./assets/1650796680204-8344869a-83a2-4e28-9936-fdc47fbc54a4.gif)
这个时候需要你当时设置Team时的密码(这块儿输入有可能是你设置Team的密码，也有可能是你电脑的屏保密码。可以尝试一下，看看哪个密码正确)
**3.9 Run一遍之后，不会报错，并且显示Build Success的提示，那你创建项目就成功了。这个时候，你连接的手机上就会出现一个空白的应用**<br />![image.gif](./assets/1650796719918-2682c505-0f32-464c-b7b8-cef149b988fd.gif)
我们现在需要到手机上的：设置-通用-描述文件与设备管理中找到你刚刚安装上的项目。点击进去，选择信任。<br />![image.gif](./assets/1650796745141-dcc411e9-f5f9-481d-b2f1-e5e1db63dff0.gif)
**3.10 我们先在Xcode里打开log日志，command+shift+y。再选择Project，再run一遍项目。连接的手机会自动弹出应用，并且会在log里打出嵌码日志。**<br />![image.gif](./assets/1650796772466-db2dc961-0e5d-434b-b5b5-b475cc98530d.gif)
![image.gif](./assets/1650796796282-c2c6c9dd-f6ee-41e1-9988-e4c2f5ebcae0.gif)
**只有出现Success to connect to NBSSERVER，才代表嵌码成功。**<br />我们再去平台上找到对应创建的应用。发现平台上有数据，IOS sdk嵌码成功。<br />![image.gif](./assets/1650796815851-6d8d204a-3577-403b-a50b-5343912c3db2.gif) 
Score: 100
"""
  },
  {
    "question": "APP如何限流？",
    "context": 
"""
可以针对应用设置一个每天的日活量进行限制。比如给A应用设备 一天10个，那么A应用每天最多只能上10个新设备，其他新设备就会被采样掉。每月清空重置。比如一个月100月活，这月用完了，下个月还是100，这个月剩余50，下个月还是100.
Helpful Answer: 可以针对应用设置一个每天的日活量进行限制。比如给A应用设备 一天10个，那么A应用每天最多只能上10个新设备，其他新设备就会被采样掉。每月清空重置。比如一个月100月活，这月用完了，下个月还是100，这个月剩余50，下个月还是100。 
Score: 50
"""
  },
  {
    "question": "APP如何限流？",
    "context": 
"""
![image.png](./assets/1655103859339-27f72121-af9c-4eb3-bb1d-b21a13c68158.png) **点次配额查看导航：**<br />系统管理-用户管理-子账号（配额）<br />**即时监测配额配置：**<br />每5分钟配额限制由500调整为1000，超过1000将会弹窗提示 ![image.png](./assets/1655104857038-f4202e99-81d2-46db-a905-0a6be08c1984.png)
Helpful Answer: "![image.png](./assets/1655103859339-27f72121-af9c-4eb3-bb1d-b21a13c68158.png) **点次配额查看导航：**<br />系统管理-用户管理-子账号（配额）<br />**即时监测配额配置：**<br />每5分钟配额限制由500调整为1000，超过1000将会弹窗提示 ![image.png](./assets/1655104857038-f4202e99-81d2-46db-a905-0a6be08c1984.png)"。
Score: 50
"""
  },
  {
    "question": "客户能不能自行注册听云账号",
    "context": 
"""

使用场景：<br />客户需要安装很多台客户端，分布在全国各地。一般情况下登录需要输入账号密码，如果客户不希望把账号密码告知全国各地的员工，则可以通过导入注册表的方式实现登陆。<br />具体实现步骤：<br />1、安装第一台客户端的时候，遵守正常安装的步骤即可。<br />2、登录客户端，输入账号密码（仅需第一台安装时）。等待登录完成
![image.png](./assets/1636342516052-6e99e4a3-070b-486a-be32-6e8d6fd3ce09.png)
3、登陆成功以后按win+r 输入regedit,进入注册表编辑<br />4、按照以下路径进行查找：<br />HKEY_LOCAL_MACHINE<br />->SOFTWARE<br />->WOW6432NODE(64位)
->NetworkBench

5、找到NetworkBench文件夹以后，右键选择导出到桌面<br />6、在本地随便找一款编辑器打开，找到serverID这个字段，删除然后保存。<br />7、接下来就是安装第二条客户端，和第一台一样，安装完以后先不要运行，双击执行一下刚才导出的注册表。点击确定

8、运行客户端，就会发现客户端不需要输入账号密码直接就进入到了正在登陆的状态。

注意事项：在安装第一台的时候，注意修改注册表中的登录地址。如果遗忘了，将会导致无法登陆。甚至如果客户连了外网，客户端会自动升级到SaaS最新版客户端
Helpful Answer: 能。
Score: 90
"""
  },
  {
    "question": "ios应用中的 页面可交互时间的方法",
    "context": 
"""
问题：相同接口的WebView 数据白屏时间差距在一倍以上，客户认为数据不准，如图

分析：<br />在同一网络环境下，使用iOS最新版本的SDK嵌入，安卓应用本身已嵌码，通过访问拍拍贷同一界面，该页面iOS使用WKWebview加载，对比数据之后，发现完全加载时间，首屏时间，可交互时间都差距较大，见下图

上图为iOS，下图为安卓<br />其中：<br />完全加载时间 = loadEventEnd - navigationStart，<br />白屏时间：WKWebview参考browser算法计算，与安卓一致，UIWebView为domLoading - navigationStart<br />首屏时间：WKWebview参考browser算法计算，与安卓一致，UIWebView与白屏时间相等<br />可交互时间 = domContentLoadEventStart - navigationStart

对比原始数据<br />发现domContentLoadEventStart与loadEventEnd都差距较大，从而导致完全加载时间、可交互时间都差距较大，而首屏时间，通过debug调试，iOS WKWebview参考browser提供的计算方法，计算后都等于白屏时间，UIWebView未提供resourceTiming接口，白屏与首屏的计算公式都为domLoading - navigationStart，故差距也较大。<br /> <br />结论：WebView性能数据不同平台差异过大的原因为系统差异，在算法相同的情况下，除了首屏、白屏、完全加载时间外，其他数据都是通过navigationTiming API获取后计算，而获取到的原始数据差异过大，从而导致数据相差过大。

ps：目前线上版本WKWebview计算的白屏时间也为domLoading - navigationStart，这种计算方式会导致白屏时间偏小，而上述测试为更改算法后的测试结果，即参考的browser算法计算，这种方式计算出来的结果与安卓相差不大，所以白屏时间可以优化，但是完全加载时间，首屏时间，可交互时间使用相同算法计算出来的时间与安卓相差仍然很大，无法调整。 
Helpful Answer: 完全加载时间 = loadEventEnd - navigationStart，\n\n白屏时间：WKWebview参考browser算法计算，与安卓一致，UIWebView为domLoading - navigationStart\n\n首屏时间：WKWebview参考browser算法计算，与安卓一致，UIWebView与白屏时间相等\n\n可交互时间 = domContentLoadEventStart - navigationStart 
Score: 90
"""
  },
  {
    "question": "what color are apples?",
    "context": 
"""
Pears are either red or orange
Helpful Answer: 从知识库无法回答此问题，请换一种问法。
Score: 0
"""
  },
  {
    "question":"APM错误数据采集原理",
    "context":
"""
## 痛点
## 思考一个问题，APM为什么要采样？
一般产品的采样有3种情况：<br />1、应用分配的资源一定的情况下，尽量减少监控所消耗的资源；（客户端）<br />2、平台的数据量太大，存储的需求太大，需要减少一些不必要的存储；（服务端）<br />3、跟商务有关系，判断是否有必要花费大价钱买全量的数据监控。（商务考虑）<br />下面主要讲一下情况1和情况2，情况3常见于app、web、小程序的售卖方式。目前与APM的关系不大。
## 情况1：探针对应用资源的消耗减少
对应的功能是探针熔断功能，其中采样是智能采样；原理是探针是否采集。<br />参考：[【APM3.0】探针熔断功能](https://tingyun.yuque.com/ngkrgt/go4s7b/gbz7oh?view=doc_embed)
## 情况2:平台数据的存储消耗的减少
对应的功能是调用链采样、请求采样；原理是collector是否丢弃一定特性的数据。
### Collector采样机制目前有两种方式：
#### 一、调用链采样
调用链采样会保留链路的完整性，开启调用链采样后，collector会根据报表上配置的采样率保留一定比例的调用链数据。例如配置了500‰，就相当于1000条调用链数据采集500条。
![image.png](./assets/1669085127602-fce2f650-a4c0-47c0-9fd5-326dc156ee59.png)
**Collector采样原理：**根据报表上配置的采样率随机采样，比如设置了500‰，**每条调用链采集的概率是1/2**，所以数据量少的时候，也可能不会成1/2的比例，比如10个调用链，只采集了3-4个，也是正常的，调用链数据越大，采集的调用链比例越接近于1/2。
**举例：**下图是3条完整的调用链，第1、3条是被采集的，第2条是被丢弃的，调用链是丢弃整条链路的数据，而不是链路上某个应用的数据。
![image.png](./assets/1669085151021-975d69c2-f24b-4a07-98c2-80fa3e065ced.png)
#### 二、请求采样
开启请求采样后，将**忽略调用链完整性**诉求，依据作用在实例级上的采样配置，**针对每次请求，保留其追踪数据**。该模式下，**链路完整性无法保证**，请谨慎开启。
![image.png](./assets/1669085163501-fa8d7bd0-1c8d-4278-a2ac-048de8a68559.png)
**Collector采样原理有两种模式：**<br />**采集模式：固定比例或者固定个数两种模式**来采集链路追踪数据。<br />**1、根据实例每分钟采集百分比的模式：**根据报表上配置的采样率随机采样，比如设置了500‰，**每条请求的采集的概率是1/2**，所以数据量少的时候，也可能不会成1/2的比例，比如10个请求，只采集了3-4个，也是正常的，请求量数据越大，采集的请求个数比例越接近于1/2。<br />**2、根据实例每分钟采集固定数的模式：**根据报表配置的采集个数采集，比如设置了10000，每分钟只保留前10000条请求数据，10000条之后的请求不保留。
举例：下图是开启请求采样前后的对比，开启前调用链路的数据完整保留，开启后调用链路的数据无法完整保留，如图只保留了链路上的A应用和D应用的请求数据。
![image.png](./assets/1669085185632-28ad672c-9b47-4cf3-b8b7-b7419abff859.png)
注：两种采样方式开启采样都不会对指标数据造成影响（比如错误、异常、数据库等），只会对调用链的数据进行采样。<br />举例：错误分析的数据依然保留，但单样本trace的数据丢弃。![image.png](./assets/1669085198759-03b8c9eb-2088-4b47-8438-490d797556bf.png)
Helpful Answer: APM采样的目的是为了减少资源消耗和存储需求
采样有三种情况：应用分配的资源有限、平台数据量太大、商务考虑
情况1：探针熔断功能，采样是智能采样，根据探针是否采集来减少资源消耗
情况2：调用链采样和请求采样，通过丢弃一定特性的数据来减少存储消耗
Collector采样机制有两种方式：调用链采样和请求采样
调用链采样保留链路的完整性，根据报表上配置的采样率保留一定比例的调用链数据
请求采样忽略调用链完整性，根据实例级上的采样配置，保留每次请求的追踪数据
采集模式有固定比例和固定个数两种模式，根据报表配置的采样率或采样个数进行采集
采样方式不会对指标数据造成影响，只会对调用链的数据进行采样
Score:90
"""
  },
  {
    "question": "智能告警能干什么？",
    "context": 
"""
## 一、背景（为什么要有告警）
 运维人员使用听云的监控，是为了保证业务平稳运行，出现问题的时候及时发现并解决问题。那么就需要持续对悟空平台的数据进行观察，那么不可能每天24小时一直刷新报表去查看数据，所以警报就出现了，可以代替人工排查，只需要配置好对应的规则，并且结合相应的通知策略，就可以在出现问题的时候及时的通过短信或者邮件等等去通知到相应的人员，及时的进行处理。  <br />**听云的智能告警➕响应模块可以实现以上内容**

## 二、配置流程
**配置流程为 告警规则 --> 推送配置(通知模版) --> 响应策略**

### 1.创建告警规则
1.1 点击告警，找到下面的配置，找到告警规则，点击右上角新建规则，点击基础告警。
![image.png](./assets/1653966361255-7e5b2709-6faf-4617-8386-6aabb59aa30b.png)
1.2 名称：XXXXX<br />适用于：响应策略和告警规则选择的范围要求一致（保证响应能匹配上）<br />告警启停：关闭了就接收不到告警<br />评估周期：可以选过去多少分钟的数据，最多可以选60分钟<br />无数据等待解除时长：告警查到没数据后，多少分钟后就解除告警<br />生效时间：这个告警在那个时间段生效<br />对象类型： 不选对象筛选就是默认对所有数据都生效，选择对象筛选就是针对某一部分的数据生效<br />告警分组：可选可不选，针对vip用户<br />对象筛选：不同对象类型提供不同的筛选维度，可以选择某一个或者全部
![image.png](./assets/1653966701814-30a87d86-2132-4e3a-867a-f7d7ea85b3ba.png)
1.3阈值检测：通过自己设置的阈值检测，超过阈值就触发告警<br />异常检测：AI判断的检测方法<br />事件检测：不是通过计算直接返回的告警事件，直接就是一个完整的告警事件<br />评估周期则是告警计算当前指标值的时候所选取样本的时间区间。<br />评估周期内超过几次则是：当不勾选的时候，指标值的计算则是整个评估周期内的平均值，例如评估周期为5分钟，则计算的为整个五分钟的平均值；如果勾选之后，会首先把评估周期以1分钟的粒度分割，每个1分钟内的样本单独计算指标值，还是列举评估周期为5分钟，那么最终计算出来的平均值有5个，每分钟有一个，超过几次就是有几个平均值超过阈值。  <br />：![image.png](./assets/1653968982649-57e77602-2a5e-400b-99da-119b1c3b59e9.png)

### 2.配置通知方式
2.1右侧管理下找到响应，点击响应里的通知模板，然后点击右上角的新建，选择需要通知的方式![image.png](./assets/1653977713093-c96b2c6a-5aed-43b9-8e06-7f7aed853e8d.png)
2.2选择的警报<br />名称：XXXXX<br />标题：XXXX<br />内容格式，txt是纯文本的格式，html是页面样式<br />邮件内容：从配置说明，更多变量模板里拿到的变量，都是固定的
![image.png](./assets/1653977956695-48c5df8a-9b06-45e4-8380-6501fb460b35.png)

### 3.接收告警
3.1右侧管理下的的响应，找到响应策略，点击右上角新建响应，选择警报，
![image.png](./assets/1653961382597-2fd6ebf1-d292-492e-8f3d-08d00f3e3683.png)
3.2响应策略：~~XXXX~~<br />使用标签过滤警报：数据源：数据的来源，产品线：响应策略和告警规则选择的范围要求一致，更准确找到那条规则，and-过滤条件。<br />规则： 根据规则控制什么情况下发通知，  
![image.png](./assets/1653966106779-64f0b0fc-ea06-4579-9aed-7d35e99bccfd.png)
3.1点击添加下一步动作，选择通用通知，选择通知的某种方式<br />注意：必须要和通知模板选择的通知方法一致
![image.png](./assets/1653978888107-88cc271c-02e6-4160-89ad-2a90d018482c.png)
接收：就是接收到告警的某个人或者某个组等<br />通知时间段：在这个时间段内接收到通知
![image.png](./assets/1653978962667-e15dcf74-abf4-4ea1-9eb3-4f4a82c17ca9.png)
成功收到通知
![image.png](./assets/1653979368644-92ac15ec-51a5-49e3-b2d2-746d9403b628.png)
Helpful Answer: 智能告警可以实现以下功能：
监控悟空平台的数据，及时发现问题
配置告警规则，根据规则触发告警
结合通知模板，通过短信或邮件等方式通知相关人员
响应策略，根据规则控制何时发出通知
可以配置多种通知方式，如短信、邮件等
可以设置通知时间段，只在指定时间段内接收通知
可以通过标签过滤告警，更准确找到对应的规则
可以配置接收人或接收组，指定谁接收告警通知
可以配置通知模板，自定义通知内容的格式和变量
可以通过配置阈值检测、异常检测、事件检测等方式触发告警
可以设置评估周期和超过几次触发告警的条件
可以配置告警的生效时间和解除时间
可以配置告警分组，针对不同用户进行告警
可以配置对象筛选，对特定的数据进行告警
可以配置无数据等待解除时长，超过一定时间没有数据解除告警
可以配置多个智能告警规则，根据需求进行灵活配置
Score: 90
"""
  },
  {
    "question": "3.0探针在2.0探针上做了哪些架构调整？",
    "context": 
"""
答：<br />1：采集与计算分离<br />APM 3.0 中将原来 2.0 的 Agent 拆分成 2 个模块，Agent + Agent Collector，Agent 只负责采集数据，Agent Collector 负责计算与数据汇总，分工明确，职责清晰。<br />2：二进制数据序列化模型<br />APM 3.0中采用 ProtocolBuffer 序列化采集数据，ProtocolBuffer具备高性能传输，低功耗的特点，可有效降低资源消耗。<br />3：基于事件的采集缓冲池技术<br />APM 3.0 中全量实时采集，基于采集完成事件，实时多线程数据发送，有效降低内存中数据停留的时间。<br />4:高性能Trace模型<br />APM3.0 中采用全新的 Trace 模型，用来实现全链路追踪。具备Decode 效率高，贯穿事务端到端，异步支持等特性。<br />5:微内核<br />APM 3.0重构探针内核，更轻薄、更稳定、更强大，具备采集业务数据的能力。
Helpful Answer: 采集与计算分离，拆分成Agent和Agent Collector两个模块
采用ProtocolBuffer序列化采集数据
使用基于事件的采集缓冲池技术
采用全新的Trace模型实现全链路追踪
重构探针内核，使其更轻薄、更稳定、更强大
Score: 90
"""
  },
  {
    "question": "主机探针部署步骤",
    "context": 
"""
# **1. 下载主机探针-linux版**
（1）登录听云平台<br />平台地址：https://apm.fesco.com   账号: liuda   密码: Tingyun@2o21<br />（2）下载主机探针<br />进入【基础设施】->【配置】->【探针管理】
![image.png](./assets/1649387157005-d75ab3a2-6a96-40c0-9893-f58e46954dba.png)
切换到【Infra Agent】，在下面选择【linux】，点击【新增】
![image.png](./assets/1649387178814-0eb2f865-2495-4263-92b4-54df7793a53a.png)
在【新增Agent】界面，选择版本（1.4.6），设置探针安装路径/data/tingyun（新创建）根据被监控主机所在位置，勾选对应Infra Collector，点击下载，获取到安装包。<br />注意: p1_collect和p2_collector为 内网使用，a1_collect和a2_collect为阿里云使用。
![image.png](./assets/1649387199077-5797a06b-e2a5-4502-939d-3cc5d300149d.png)
点击生成安装脚本，然后点击“copy”，
![image.png](./assets/1649387214340-b5f6b2d3-7c0f-4e79-98c7-f891d9754545.png)
将指令拷贝到目标主机命令提示符中，目标主机的命令执行路径与上面指定的探针安装路径：/data/tingyun，并进行修改，将其中的两个collector ip地址改为域名：
![image.png](./assets/1649387235425-0062b944-20f6-4b4d-a35f-cb7039fe9f62.png)
注意：此处的域名需要根据目标主机所在的资源位置来设置。<br />私网collector域名：<br />apm-infra-collector1.fesco.com.cn       10.0.76.184<br />apm-infra-collector2.fesco.com.cn       10.0.76.185<br />互联网collector域名：<br />apm-infra-collector1.fesco.com.cn        79.21.1.201<br />apm-infra-collector2.fesco.com.cn        79.21.1.202<br />返回听云平台，点击第5步的“copy”，执行校验：
![image.png](./assets/1649387246564-9aa06b81-2baa-4d80-9d1c-1284fbc415f5.png)
![image.png](./assets/1649387279111-9227eed3-aaf4-4f1d-a57e-bc57241bb638.png)

结果提示“passed”。<br />点击“copy”，将脚本执行命令拷贝到目标主机执行。
![image.png](./assets/1649387293811-acbb6f9f-90ff-488e-bd4e-f096893ded5e.png)
执行完成：
![image.png](./assets/1649387310499-5288f31b-e19d-40d4-a342-0dbe7020df33.png)
查看服务运行状态：
![image.png](./assets/1649387326604-ab1d7165-d42c-4416-9d19-c568a6789661.png)

# **2. 安装主机探针-linux版到目标主机**
下面以linux机器：10.0.76.184为例说明<br />（1）以超级管理员角色登录（root）<br />（2）在/data/tingyun下执行在上面步骤中获取的相关指令。<br />（3）执行安装命令
![image.png](./assets/1649387356629-702cb3b5-d397-40d7-bdd4-e4e17c28e9d3.png)
（4）查看服务运行状态：
![image.png](./assets/1649387368654-6ac888df-d761-4663-a02b-b1484932ebf1.png)**3. 验证主机探针是否部署成功**<br />（1）在目标主机中运行命令：ps -ef|grep agent 查看到相关进程信息
![image.png](./assets/1649387386407-37f997ca-23ed-4a39-8a7a-db8f2c321d05.png)
（2）进入探针日志目录：/data/tingyun/agent/node_exporter/logs
![image.png](./assets/1649387397325-ac2ed618-4ded-4a4b-8db0-37c604f5edc6.png)
查看探针运行日志
![image.png](./assets/1649387413273-c6cc2bdd-5dc1-4309-8582-483b93bea3e7.png)
查看探针监测信息：<br />命令行执行curl 10.0.76.184:19109/metrics
![image.png](./assets/1649387429834-a151d1d6-93e4-45c3-ad84-8a621d1c471c.png)

（3）返回听云平台，进入【基础设施】->【配置】->【探针管理】，切换到【Infra Agent】，在下面选择【linux】，查看以部署主机探针的目标主机。<br />（4）进入【基础设施】->【主机监控】->“linux”，稍等会，目标主机的CPU、内存、磁盘容量等信息将显示出来。
![image.png](./assets/1649387447578-b7c628dc-3436-4a6a-b404-0ea4a83b7504.png)
至此，一台linux主机的主机探针部署完成。

# **4. 注意**
在1.下载主机探针-linux版中获取的探针包可拷贝的其他linux目标主机上进行重复使用，无需重复在听云平台下载。注意：仅限在主机类型及主机所在资源位置一致的情况下使用。
Helpful Answer:登录听云平台，进入【基础设施】->【配置】->【探针管理】
切换到【Infra Agent】，选择【linux】，点击【新增】
选择版本（1.4.6），设置探针安装路径为/data/tingyun，并根据被监控主机所在位置选择对应的Infra Collector
点击生成安装脚本，将指令拷贝到目标主机命令提示符中，并修改其中的collector IP地址为对应的域名
返回听云平台，点击第5步的“copy”，执行校验
将脚本执行命令拷贝到目标主机执行
查看服务运行状态，确认探针部署成功
验证探针部署是否成功，查看进程信息、探针日志和监测信息
返回听云平台，查看已部署主机探针的目标主机
进入【基础设施】->【主机监控】，查看目标主机的监测信息
Score: 90
"""
  },
  {
    "question": "【java探针】定制化容器如何部署？",
    "context": 
"""
## 由于每个客户的容器定制情况都不一样，该文档主要是提供一个在定制化容器下部署的思路，仅供参考。

## 环境信息
容器：定制版tomcat<br />系统：linux<br />探针：Java探针

## 部署思路
1、先跟客户研发语音沟通一下，问清楚客户启动脚本加JVM参数的地方在哪，把我们探针嵌码加到客户的JVM参数前即可。<br />2、由于客户是定制化的tomcat，客户使用变量的方式引入参数，如图所示（这些信息需要跟客户确认，如果客户不知道，就得我们自己远程去查看客户的脚本文件有什么不一样的地方）。
![image.png](./assets/1640748420617-55d62d4d-2a74-430f-84f7-60a5a53c5972.png)
3、搜索javaagent，在下图位置添加我们探针嵌码，格式和客户的变量格式要一致，采用双斜杠。
![image.png](./assets/1640748538284-94fd0103-1e68-49ea-bb48-591bf4d41946.png)

## 注意事项
1、确认客户的JVM参数加载的位置。<br />2、确认客户定制化的tomcat脚本的格式。<br />3、确认客户的启动方式。
Helpful Answer: 先跟客户研发语音沟通一下，问清楚客户启动脚本加JVM参数的地方在哪，把我们探针嵌码加到客户的JVM参数前即可。
由于客户是定制化的tomcat，客户使用变量的方式引入参数，需要在相应位置添加我们探针嵌码，格式和客户的变量格式要一致，采用双斜杠。
注意确认客户的JVM参数加载的位置、定制化的tomcat脚本的格式以及客户的启动方式。
Score: 90
"""
  }
]


example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS,
    # This is the number of examples to produce.
    k=1
)



