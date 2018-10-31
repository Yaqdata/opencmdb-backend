# OpenCMDB
  - 产品定位：全开源轻量级CMDB项目
  - 我们的口号：让中国所有的运维工程师不再使用Excel管理运维资产！
  - 官网网站： http://opencmdb.cn
  - 前端代码：https://github.com/unixhot/opencmdb-frontend/
  - 后端代码：https://github.com/unixhot/opencmdb-backend/
  - 项目成员：赵班长（PO）、母红英（Dev）、张亚庆（Dev）、张龙（Dev）
  

## 系统组件和引用说明
 
- 前端框架：Vue.js https://cn.vuejs.org/ 
- 数据可视化：Echarts http://echarts.baidu.com/
- 后端：Flask + Flask Restful + Mongodb
- API文档：Swagger UI https://swagger.io/download-swagger-ui/
- API测试：pyresttest https://github.com/svanoort/pyresttest
- RESTful API设计指南： http://www.ruanyifeng.com/blog/2014/05/restful_api.html

## 主要模块

- 模型管理（自定义CI模型、模型编辑、模型关系等） v0.1 - 当前版本
- 仓库管理（基于Excel数据导入导出、资产编辑、资产搜索、Web SSH等） v0.2
- 视图管理（内置架构视图、业务视图等） v0.2
- 容量管理（多维度Dashboard展示） v0.3
- 系统设置（API Token、验证方式、） v0.3
- 用户中心（权限管理、SSH Key管理） v0.3


## 安装文档
    
### API简介

API主要使用：

- [Flask](http://flask.pocoo.org/)
- [Flask-Security](https://flask-security.readthedocs.io/en/latest/)
- [Flask-MongoEngine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)
- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
- [Arrow](http://arrow.readthedocs.io/en/latest/)

### 本地测试环境搭建


1.安装Python 3.6

```
[root@linux-node1 ~]# yum install https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm
[root@linux-node1 src]# yum install -y gcc glibc make zlib-devel openssl-devel curl-devel
[root@linux-node1 ~]# cd /usr/local/src
[root@linux-node1 src]# wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz
[root@linux-node1 src]# tar zxf Python-3.6.6.tgz
[root@linux-node1 src]# cd Python-3.6.6/
[root@linux-node1 Python-3.6.6]# ./configure --prefix=/usr/local/Python-3.6.6 --with-ssl
[root@linux-node1 Python-3.6.6]# make && make install
```

2.创建Python虚拟环境,并安装依赖

```
[root@linux-node1 opt]# /usr/local/Python-3.6.6/bin/pyvenv-3.6 opencmdbENV
[root@linux-node1 ~]# cd /opt/
[root@linux-node1 opt]# git clone http://gitlab.devopsedu.com/opencmdb/opencmdb-backend.git
[root@linux-node1 ~]# source /opt/opencmdbENV/bin/activate
(opencmdbENV) [root@linux-node1 ~]# pip install -r /opt/opencmdb-backend/requirements.txt 

```

3.安装MongoDB

```
[root@linux-node1 ~]# yum install -y mongodb mongodb-server
[root@linux-node1 ~]# systemctl start mongod
[root@linux-node1 ~]# netstat -ntlp | grep 27017
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      28513/mongod
[root@linux-node1 ~]# mongo
> use opencmdb
switched to db opencmdb
> db.createUser({user: "opencmdb",pwd: "opencmdb",roles: [ { role: "readWrite", db: "opencmdb" } ]});
Successfully added user: {
	"user" : "opencmdb",
	"roles" : [
		{
			"role" : "readWrite",
			"db" : "opencmdb"
		}
	]
}

```

4.修改配置文件并启动


```
[root@linux-node1 ~]# cd /opt/opencmdb-backend/
[root@linux-node1 ~]# source /opt/opencmdbENV/bin/activate
#指定使用development的配置
export FLASK_ENV=DEVELOPMENT

#设置配置文件
 (opencmdbENV) [root@linux-node1 opencmdb-backend]# cp api/config/development.py_sample api/config/development.py
 (opencmdbENV) [root@linux-node1 opencmdb-backend]# vim api/config/development.py
 #(编辑api/config/development.py 更改mongo的配置, 任意配置SECRET_KEY和SECURITY_PASSWORD_SALT)

 #执行 python manager.py init_user_info 初始化用户信息
(opencmdbENV) [root@linux-node1 opencmdb-backend]# python manager.py init_user_info
(opencmdbENV) [root@linux-node1 opencmdb-backend]# python manager.py runserver -h 0.0.0.0 -p 6000

```

5.配置swagger

- 修改 `./swagger/index.html` 44行 将地址配置为自己的服务地址
- 修改 `./swagger/public/api.ymd` 12行 将地址配置为自己的服务地址


# DevOps Flow：该项目使用DevOps-X进行管理

### 项目管理：
1. 使用Redmine进行项目管理，采用敏捷开发方式。

### 分支管理：

1. 采用特性分支策略，每一个用户故事对应一个特性分支。

### 流水线设计：

1. 提交阶段流水线：采用特性分支，除Master外分支有任何Push操作，即触发。
2. 基础测试阶段流水线：采用Docker进行测试，Master分支有Push操作，即触发。
3. 生产部署阶段流水线：采用Kubernetes进行发布
 
