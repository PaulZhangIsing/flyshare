# Flyshare

### 简介

Flyshare是实现对全球股票/期货等金融数据从数据采集、清洗加工 到 数据过滤的工具，
满足金融量化分析师和学习数据分析的人在数据获取方面的需求，
Flyshare的特点是数据覆盖范围广，接口调用简单,响应快速。

### 获得验证码

为了更好的为用户群体提供服务，我们提供验证码让用户可以方便的使用，请到如下页面注册获得验证码： [注册页面](http://www.asiabigdata.org/registration/)。

用户可以在这里找到直接的验证码：[验证码页面](http://www.asiabigdata.org/login/).

#### 验证码使用方式
导入Flyshare的模块后，可按照如下方式设置api_key即可开始使用我们免费提供的数据: 
```
import flyshare
flyshare.ApiConfig.api_key = "YOURAPIKEY"
```

### 免费数据
Flyshare 收集了广泛的数据源，为用户提供一个简单、方便、易于使用的数据接口。


### 项目安装

**方法1**

在[这里](https://github.com/duanrb/flyshare)下载最新版本:

* Windows：双击运行install.bat自动安装
* Ubuntu：在Terminal中运行bash install.sh自动安装

**方法2**
也可以使用pip 安装 flyshare
```bash
pip install flyshare
import flyshare 
```

### Tutorial

tutorial目录下的 tutorial.ipynb 是一个简单的的例子
