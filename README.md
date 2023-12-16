# 电影管理系统movie management system

![功能预览](_doc/功能.jpg)

hyx

数据库系统概论大作业

20231106

## 特色

- 同步连接：SQL server两个数据库movie_info和actor_info
- 基础功能实现：实现的查询、添加、修改、删除

- 交互性强：成功失败都有弹窗反馈，删除会有二次确认
- 界面美观：符合现代审美

## 实现

- 数据库：SQL server
- 编程语言：Python
- Web 框架：Flask
- 前端框架：Bootstrap5

## 参考

[RUCstore](https://git.ruc.edu.cn/gengdy/rustore)

[Flask 入门教程 3.0](https://helloflask.com/book/3/)

[Bootstrap5 中文手册](https://www.bootstrap.cn/doc/book/2.html)

## Flask学习过程

https://github.com/Silverwolf-x/study-flask.git

## 构建历史

20231124
重构项目文件夹结构，编辑初始化数据库相关内容；暂定实现的内容

20231202
基于flask-Bootstrap5完全重写前端，重写后端框架。现已做到查询、新建、删除功能

20231203

- 正式发布version-alpha

实现movie_info和actor_info两个表分别的查询、编辑、新建、删除

记得使用utf8编码的sql初始化数据

20131216
- 编辑主页，修改框架，正式发布version 1.0
- 分离search,edit,add的form，完备验证模块，发布version 1.1