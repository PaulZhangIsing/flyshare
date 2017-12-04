#快速使用Docker建立Flyshare执行环境

<!-- TOC -->
- [快速使用Docker建立Flyshare执行环境](#快速使用Docker建立Flyshare执行环境)
    - [获取安装了Flyshare的镜像](#获取安装了Flyshare的镜像)
    - [从头安装Flyshare](#从头安装Flyshare)

<!-- TOC -->

##快速使用Docker建立Flyshare执行环境

首先，到[docker网站](https://www.docker.com/)下载相应的版本，并创建账号（注意：登录docker账号才能下载镜像）

执行以下命令获取镜像
```shell
docker pull duanrb/flyshare
```

下载镜像后执行
```
docker run -it duanrb/Flyshare bash
```

然后在docker容器中执行以下命令
```
ipython

```
 
##从头安装Flyshare

可以从一个干净的ubuntu镜像上开始安装，获取ubuntu镜像
```angular2html
docker pull ubuntu
```
然后按照[Flyshare 安装说明](../README-cn.md)进行安装