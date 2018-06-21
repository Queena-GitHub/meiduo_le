# 修改Django原来提供的异常处理功能[补充mysql和redis的处理异常]

from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取在配置文件中定义的logger，名称为django的日志记录器，用来记录日志
logger = logging.getLogger('django')

# 调用rest框架提供的异常处理方法
def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    # 如果系统没有报错或者报错的类型不是drf框架识别的，那么返回值都是None
    if response is None:
        view = context['view']
        # 如果是数据库错误或者是redis错误
        # 如果exc对象是DatabaseError的实例，或者exc是RedisError的实例
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 记录数据库异常
            logger.error('[%s] %s' % (view, exc))
            # 返回json对象给前端，507，系统内部错误
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response

