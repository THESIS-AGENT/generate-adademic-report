import os
import signal
import functools
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import concurrent.futures
import threading

# 定义 with_timeout 装饰器
def timeout_handler(signum, frame):
    """超时信号处理函数"""
    raise TimeoutError("操作超时")

def with_timeout(timeout_param=None, default_seconds=120):
    """函数超时装饰器
    
    修改为始终使用ThreadPoolExecutor实现超时功能，
    因为signal模块只能在主线程中使用。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 确定超时时间
            seconds = default_seconds
            if timeout_param and timeout_param in kwargs:
                seconds = kwargs[timeout_param]
            
            # 使用线程池实现超时
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    raise TimeoutError(f"函数 {func.__name__} 执行超时（{seconds}秒）")
                
        return wrapper
    return decorator
