# ucas

ucas 选课脚本，支持轮询选课，当有人退课时自动选课

## 安装

### 环境依赖

Python 2.x

### Mac

```bash
brew install python
sudo easy_install pip
sudo pip install requests
```

### Linux

```bash
sudo apt install python-pip
sudo pip install requests
```

### Windows

官网中安装Python后安装requests

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
091M5023H
091M4002H
```

config文件中共有三个配置，单次请求等待时间，轮询最短时间和轮询最长时间，可根据需求修改

## 持久运行

非校园网环境登录需要验证码，须长期轮询是否有人退课时，可在校园网（无验证码）的环境下运行该脚本登录，此时目录下会生成cookie.pkl文件，把该文件放置在服务器中在服务器中保留登录状态。
