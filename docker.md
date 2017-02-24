# docker的极简入门指南（数据分析及数据挖掘方向）

## 一：为什么要用docker？

* 一些使用windows系统的用户在安装python库、tensorflow、xgboost等时经常遇到安装不了或者编译问题等，使用docker可以在用windows的情况下获得linux环境，方便各种库的编译
* 解决python环境污染问题，并方便保持各种库为最新状态

## 二：docker 的简单入门教程
[docker是什么，官方说这叫容器，但确实难以理解，入门的把它理解为轻量级虚拟机就好，它其实是一个相当易用的软件，本文不教太多命令，因为我也不会，只会讲几个基本命令。如果用linux的肯定会下载安装docker，本文就讲讲如何在windows10下如何安装使用docker]

1. 下载安装docker

首先当然是去官网下载啦，进入www.docker.com，点击图上的图标，我们可以看出如果用win10那么你必须要安装专业版或者旗舰版，家庭版的win10只能悲剧去和win7一样安装就docker toolbox啦，这里就不展开讲了。默认你是win10专业版，如果你不是，那么你就变身吧......
2. 下载安装docker
这个一般就只有下一步下一步，过
3. 启动docker
点击桌面的这个图标就启动起来了
4. 拉取镜像
打开cmd输入以下命令拉取kaggle官方制作的一个镜像，里面封装好了xgboost、anaconda、tensorflow等常用的库及软件，而且kaggle还会不断的更新，省的自己来update

```docker pull kaggle/python```
要下载几个G，安心等吧，如果下不了那么就去daocloud[http://get.daocloud.io/]注册个账号弄个加速吧。
5. 建立一个文件夹来交换文件
比如说我们在d盘建立一个kaggle文件夹来交互文件，继续在cmd中输入下面的命令进入d盘

```cd /d d:```

然后新建一个文件夹叫做kaggle
```mkdir kaggle```
那么我们的需要交互的文件夹的就钦定“D:/kaggle”了
6. 运行镜像

```docker run --name kaggle  -v D:/kaggle:/tmp/working/kaggle  -w=/tmp/working -p 8888:8888 -d  -it kaggle/python  jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/tmp/working``` 
简单解释一下  --name kaggle 代表我们给它起名叫kaggle 制定一个交换目录是win下的d:/kaggle 和 linux下的/tmp/working/kaggle 端口号为8888，-d 代表在后台运行  ，jupyter notebook --no-browser 代表不用浏览器的方式运行notebook，
7. 运行notebook
这个时候用你win10的自己装的浏览器就可以访问notebook了，而且访问的是docker里的notebook
8. 输入notebook 的code
docker exec -it kaggle bash
9. 停止容器
docker stop kaggle