# UCAS

ucas 选课脚本，支持轮询选课，当有人退课时自动选课。

> 注：每年网站代码可能会变动，因作者无选课权限，且SEP不提供预选测试，故脚本存在失效可能，请注意风险。推荐在选课前查看本仓库代码是否有更新，并通过登录等功能对代码进行测试。如果在选课过程中发现课程的CollegeCode或选课网站的API有更新，欢迎发起PR或issue，非常感谢。

## 安装

### 环境依赖

Python 3.x

### Mac

```bash
brew install python3
sudo easy_install pip
sudo pip install requests
```

### Linux

```bash
sudo apt install python3-pip
sudo pip install requests
```

### Windows

[官网](https://www.python.org/downloads/)中安装Python后安装requests

```bash
python -m pip install requests
```

## 初始化

在当前目录下创建 `auth` 文件并填入登录信息，格式如下：

```
i@iie.ac.cn
inputpassword
```

第一行为用户名，第二行为密码

在当前目录下创建 `courseid` 文件并填入课程，格式如下：

```
091M5023H,xx学院
091M4002H
```

其中`xx学院`可选（建议填写），课程号与学院名称间用`,`分隔（注意中英文符号），学院名必须与选课系统上的名称部分匹配。
例如英语课是"外语系"开课，那么可以填"外语系"或"外语"，但不能填"外国语"

截止至2021年01月18日，选课系统上有效的学院名称：
- 数学学院
- 物理学院
- 天文学院
- 化学学院
- 材料学院
- 生命学院
- 地球学院
- 资环学院
- 计算机学院
- 电子学院
- 工程学院
- 经管学院
- 公管学院
- 人文学院
- 马克思主义学院
- 外语系
- 中丹学院
- 国际学院
- 存济医学院
- 体育教研室
- 微电子学院
- 未来技术学院
- 网络空间安全学院
- 心理学系
- 人工智能学院
- 纳米科学与技术学院
- 艺术中心
- 光电学院
- 创新创业学院
- 核学院
- 现代农业科学学院
- 化学工程学院
- 海洋学院
- 航空宇航学院
- 杭州高等研究院

config文件中共有三个配置，单次请求等待时间，轮询最短时间和轮询最长时间，可根据需求修改

## 持久运行

非校园网环境登录需要验证码，须长期轮询是否有人退课时，可使用 ``python enroll.py -c`` 命令运行， 此时会在目录下生成captcha.jpg文件，根据该图片的内容输入验证码即可登录。

## 邮件提醒

需要邮件提醒时，在当前目录下创建 `mailconfig` 文件并填入登录信息，格式如下：

```
i@iie.ac.cn
inputpassword
mail.cstnet.cn
i@iie.ac.cn
```

第一行为邮箱用户名，第二行为邮箱密码，第三行为SMTP服务器地址，第四行为接收通知邮件的邮箱。

创建完成后，带 `-m` 参数运行即可在选课结束后发信通知。

注：

1. 网易系邮箱第三方不能使用密码登录，需单独设置授权码。
2. 学校邮箱服务器为 `mail.cstnet.cn`

## 更新概要

- `2021-09-03` 选课系统加入了CSRF Token与Referer验证，[Yangjiaxi](https://github.com/Yangjiaxi) 更新了对应的逻辑

- `2021-09-01` [KLOSYX](https://github.com/KLOSYX) 发现SEP系统更新了验证码地址，提交[issue](https://github.com/LyleMi/ucas/pull/10)进行了维护

- `2021-01-18` [Cirn09](https://github.com/LyleMi/ucas/pull/6) 增加了Python3支持，增加了自动重新登录等特性，添加了新的courseId格式

- `2019-08-29` [pzhxbz](https://github.com/LyleMi/ucas/pull/3) 更新了CollegeCode

- `2018-09-06` 参考前人的代码完成选课功能，增加重试等特性
