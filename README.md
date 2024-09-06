<div align="center">

# ともたけ よしの bot
*********************

_🌱 This project is based on the [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) and [fnbot](https://github.com/lynvtiki/yoshino-bot) development of QQ entertainment robot 🌱_

</div>

<div align="right">
  语言 | Language:
  <a title="Chinese" href="/README.md">🇨🇳</a>
  <a title="English" href="/docs/README_en.md">EN</a>
</div>



# Quick Start
- 此项目用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)作为前端,
  python3作为后端, 搭建的QQ机器人
- 核心代码集中放在`fnbot`文件夹中, 方便导入使用
- 插件代码集中放在`plugins`文件夹中, 方便管理



# Chatgpt Analysis Report

使用chatgpt解析本项目, 如果有问题那就怪chatgpt

- [CN](https://github.com/lynvtiki/yoshino-bot/blob/master/docs/chatgpt_analysis_report.md)
- [EN](https://github.com/lynvtiki/yoshino-bot/blob/master/docs/chatgpt_analysis_report_en.md)



# for Windows

## 下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

- 启动后注意选择`0: HTTP通信`

- 如果第一次使用, 可以先看看[官方文档(点我)](https://docs.go-cqhttp.org/guide/#go-cqhttp)

- 修改生成的`config.yml`

  <details>
  <summary>需要修改的内容</summary>

  ```yml
  account: # 账号相关
    uin: 123456789 # QQ账号
    password: '' # 密码为空时使用扫码登录
  ```
  and
  ```yml
  # 连接服务列表
  servers:
    # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
    #- http: # http 通信
    #- ws:   # 正向 Websocket
    #- ws-reverse: # 反向 Websocket
    #- pprof: #性能分析服务器

    - http: # HTTP 通信设置
        address: 127.0.0.1:9900 # HTTP监听地址
        timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
        long-polling:   # 长轮询拓展
          enabled: false       # 是否开启
          max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
        middlewares:
          <<: *default # 引用默认中间件
        post:           # 反向HTTP POST地址列表
        #- url: ''                # 地址
        #  secret: ''             # 密钥
        #  max-retries: 3         # 最大重试，0 时禁用
        #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
          - url: http://127.0.0.1:9901/ # 地址
            secret: ''                  # 密钥
            max-retries: 10             # 最大重试，0 时禁用
            retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
  ```

  </details>

## 下载和配置python代码

```powershell
cd qqbot
```

```powershell
git clone https://github.com/lynvtiki/yoshino-bot
```

```powershell
cd yoshino-bot
python -m pip install -r requirements.txt
```

- 临时换源
```powershell
python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

- 修改`pybot.toml`
  <details>
  <summary>需要修改的内容</summary>

  ```toml
  host = "127.0.0.1"
  port = 9900 # 对应gocq的config.yml中的 address: 127.0.0.1:9900
  post = 9901 # 对应gocq的config.yml中的 - url: http://127.0.0.1:9901/
  bot_qq = 123456789 # qq账号
  group_list = [123456,1234567] # 需要添加的qq群号
  ```

  </details>

## 最后运行`main.py`

```powershell
python main.py
```

---

# 建议

- 新建配置文件`config.toml`或`config.json`替代`pybot.toml`或`pybot.json`

- 新建`bot.py`文件代替`main.py`

---

# for Linux

## 预先安装`python3和git`(`可跳过`)

```bash
apt install python3
apt install git
```

---

## 下载`gocq`
- 可手动可命令两种方式下载, 这里选择命令的方式
- 这里以`arm`架构为例

```bash
mkdir qqbot
cd qqbot
mkdir gocq
cd gocq
wget https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc5/go-cqhttp_linux_arm64.tar.gz
tar -xvf go-cqhttp_linux_arm64.tar.gz
./go-cqhttp
```

- 选择`0: HTTP通信`

- 修改的配置信息和上面在windows配置的一样

> 也可以使用别的修改, 这里以`vim`为例
>
> `vim config.yml`这条命令执行完后, 会进入新的界面
>
> 输入`i`键后进入编辑模式, 点`esc`键退出编辑模式
>
> `h`左移光标, `j`下移光标, `k`上移光标, `l`右移光标
>
> 如果需要退出并保存, 点`esc`后, 依次输入`:`, `w`, `q`, 回车
>
> 如果`:wq`退出保存不了, 使用`:wq!`强制退出并保存

```bash
vim config.yml
./go-cqhtttp
```

## 注意,如果使用的是`termux`, 最新版本的gocq会出点小问题

- 可使用`termux-chroot`避免这个bug

```bash
termux-chroot
./go-cqhttp
```

## 下载和配置python代码

- 修改的配置信息和上面在windows配置的一样

```bash
cd qqbot
```

```bash
git clone https://github.com/lynvtiki/yoshino-bot yoshino-bot
```

```bash
cd yoshino-bot
python -m pip install -r requirements.txt
```

`临时换源`
```bash
python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

```bash
vim pybot.toml
```

```bash
python3 main.py
```
