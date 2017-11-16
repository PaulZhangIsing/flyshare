# Flyshare

### 简介

Flyshare是一个简化多种数据源的数据中间件

### 验证码

为了更好的为用户群体提供服务，我们提供验证码让用户可以方便的使用，请到如下页面登记获得验证码： [验证码页面](http://www.asiabigdata.org/registration/)。

用户可以在这里找到直接的验证码：[账户设置页面](http://www.asiabigdata.org/login/).

#### 验证码使用方式
导入Flyshare的模块后，可按照如下方式设置api_key即可开始使用我们免费提供的数据: 
```
import flyshare
flyshare.ApiConfig.api_key = "YOURAPIKEY"
```

### 免费数据
Flyshare 收集了广泛的数据源，尽量为用户提供一个简单、方便、易于使用的数据接口。


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
