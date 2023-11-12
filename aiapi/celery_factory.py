# -*- coding: utf-8 -*-
"""
@author:lpf
@file: celery_factory.py
@time: 2023/7/27  17:22
"""
import os

from celery import Celery

# 设置django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiapi.settings') # 项目配置

# 创建celery实例化对象
app = Celery('aiapi')   # 项目名

# 启动项目celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现项目中的tasks
app.autodiscover_tasks()
