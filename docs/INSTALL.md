## Install
    
### 简介

API主要使用：

- [Flask](http://flask.pocoo.org/)
- [Flask-Security](https://flask-security.readthedocs.io/en/latest/)
- [Flask-MongoEngine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)
- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
- [Arrow](http://arrow.readthedocs.io/en/latest/)

### 本地测试环境搭建


搭建python 3.6 环境, 以及安装mongodb

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

执行 python manager.py init_user_info 初始化用户信息
(opencmdbENV) [root@linux-node1 opencmdb-backend]# python manager.py init_user_info


```

4.配置swagger

- 修改 `./swagger/index.html` 44行 将地址配置为自己的服务地址
- 修改 `./swagger/public/api.ymd` 12行 将地址配置为自己的服务地址
