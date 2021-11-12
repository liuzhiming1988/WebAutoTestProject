#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : decorators.py
@Author  : liuzhiming
@Time    : 2021/11/4 10:11
"""
import sys
import traceback
from functools import wraps


# 捕捉异常装饰器
def try_except(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_str = 'Function name: {0}; Error info: {1}: {2}; Traceback: {3}'\
                .format(str(fn.__name__),
                        str(e.__class__.__name__),
                        str(e),
                        str(traceback.extract_tb(exc_tb)))
            raise
            # 正式环境，记录错误日志并返回错误信息
            # if not app.config['DEBUG']:
            #     LOGGER.exception_log(error_str)
            #     return jsonify({'success': False, 'error': str(e)})
            # 测试环境直接raise
            # else:
                # raise
    return wrapped


