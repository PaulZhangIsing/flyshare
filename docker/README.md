# Flyshare 的 Docker 镜像

author: [@duanrb](https://github.com/duanrb) 



Docker 常用命令示例：
```
docker build -t friendlyname .  # Create image using this directory's Dockerfile
docker run -p 4000:80 friendlyname  # Run "friendlyname" mapping port 4000 to 80
docker run -d -p 4000:80 friendlyname         # Same thing, but in detached mode
docker ps                                 # See a list of all running containers
docker stop <hash>                     # Gracefully stop the specified container
docker ps -a           # See a list of all containers, even the ones not running
docker kill <hash>                   # Force shutdown of the specified container
docker rm <hash>              # Remove the specified container from this machine
docker rm $(docker ps -a -q)           # Remove all containers from this machine
docker images -a                               # Show all images on this machine
docker rmi <imagename>            # Remove the specified image from this machine
docker rmi $(docker images -q)             # Remove all images from this machine
docker login             # Log in this CLI session using your Docker credentials
docker tag <image> username/repository:tag  # Tag <image> for upload to registry
docker push username/repository:tag            # Upload tagged image to registry
docker run username/repository:tag                   # Run image from a registry
```
> - Docker加速看[这里](https://www.daocloud.io/mirror#accelerator-doc)
> - Docker教程看[这里](https://yeasy.gitbooks.io/docker_practice/content/)。

## 设计概述

1. 使用 docker 镜像来提供基于 flyshare 的交易系统开发、测试、回测、实盘环境。

2. 将策略打包到 docker 镜像中以便直接在生产环境部署。


## 镜像制作与实例运行

### 制作环境镜像
在`docker/`目录下运行:

```bash
➜  docker build -f Dockerfile --force-rm -t flyshare ..
...
Successfully built 8w3jjofejeaij
```

漫长的等待后之后，查看
```bash
➜  docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED                  SIZE
flyshare                      latest              8w3jjofejeai        Less than a second ago   3.02GB
ubuntu                        16.04-tools         1196ea15dad6        5 months ago             336MB
```

flyshare 的运行环境镜像 `flyshare:latest` 制作成功。
之后可以使用该镜像继续构建下层镜像，用于生产环境的部署。
