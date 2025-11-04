# Raspberry Pi Zero 2W Photo Album

## 项目简介

这是一个基于 **Flask** 的树莓派 Zero 2W 本地照片相册项目，特点如下：

- 自动轮播照片，支持本地照片管理  
- 支持通过 Web 界面查看和管理照片  
- 使用 SQLite 数据库存储照片信息  
- 全部运行在树莓派 Zero 2W，无需额外服务器  
- 支持开机自启动（通过 Systemd service 和 feh 播放轮播）

---

## 项目结构

```

photo_album/
├─ app.py               # Flask 主程序
├─ init.py              # 初始化脚本
├─ database_init.py     # 数据库初始化脚本
├─ photo_album.db       # SQLite 数据库
├─ photos/              # 存放照片
├─ templates/           # HTML 模板
├─ static/              # 静态资源（CSS / JS / 图片）
├─ photo_album.service  # Systemd 服务文件
└─ venv/                # Python 虚拟环境

````

---

## 功能说明

### 照片管理

- 上传、删除照片  
- 自动轮播显示照片（使用 `feh` 播放器）  
- 支持照片缩放，适配屏幕大小  

### Web 界面

- Flask 提供的管理界面  
- 查看照片列表和轮播效果  
- 可在浏览器中操作：`http://<pi-zero-ip>:5000`  

### 数据存储

- 使用 SQLite 数据库存储照片信息  
- `database_init.py` 可初始化数据库  

### 开机自启动

- 使用 `photo_album.service` 注册为 systemd 服务  
- 系统启动时自动运行照片轮播与 Web 服务器  

**示例 `photo_album.service` 内容：**

```ini
[Unit]
Description=Pi Zero2W Photo Album Slideshow + Webserver
After=network.target graphical.target

[Service]
User=pi
Type=simple
WorkingDirectory=/home/pi/photo_album
ExecStart=/bin/bash -c "sleep 10; DISPLAY=:0 /usr/bin/feh --fullscreen --slideshow-delay 10 photos/"
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
````

---

## 安装与运行

1. **安装依赖**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv feh -y
```

2. **创建虚拟环境并安装 Python 依赖**

```bash
cd ~/photo_album
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **初始化数据库**

```bash
python3 database_init.py
```

4. **运行项目**

```bash
python3 app.py
```

访问浏览器：`http://<pi-zero-ip>:5000`

5. **设置开机自启动（可选）**

```bash
# 复制服务文件到 systemd 目录
sudo cp photo_album.service /etc/systemd/system/

# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start photo_album

# 设置开机自启动
sudo systemctl enable photo_album

# 查看服务状态
sudo systemctl status photo_album
```

---

## 配置说明

* 照片存放路径：`photos/`
* 数据库文件：`photo_album.db`
* 模板目录：`templates/`
* 静态文件目录：`static/`

---

## 技术栈

* Python 3
* Flask
* SQLite
* HTML / CSS / JavaScript
* feh（轮播显示照片）

---

## 注意事项

* 项目为树莓派 Zero 2W 优化，避免使用过大照片导致卡顿
* 建议每张照片分辨率不超过 1024x768
* Systemd 服务中的 `DISPLAY=:0` 假设你使用的是 HDMI 显示器，如有不同需修改

---

## License

This project is licensed under the **Apache License 2.0**.
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).