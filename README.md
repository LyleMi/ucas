# ucas

ucas 选课脚本

## 安装

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
