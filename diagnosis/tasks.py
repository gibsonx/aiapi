from celery import Celery
from celery.schedules import crontab
import time
import os
from celery import Celery
from celery import shared_task
# 设置django环境变量
from aiapi.celery_factory import app
# 普通任务 由 方法名 send_email.delay()触发
@shared_task()
def send_email(level, content):
    print('去数据库根据等级查询用户:'+"_".join(level))
    print('发送的内容为：' + content)
    time.sleep(20)
    print('发送邮箱结束')
    return "send_email success"
