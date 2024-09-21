import os
import logging
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor

from bebinca.configs import settings

executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池


class ThreadPoolHandler(logging.Handler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler

    def emit(self, record):
        executor.submit(self.handler.emit, record)  # 将日志记录任务提交到线程池中


app_env = settings.env
app_name = settings.app_name

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_file_handler():
    basedir = settings.basedir
    log_dir = os.path.join(basedir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'bebinca.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    return file_handler


def create_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    return console_handler


handler_funcs = {
    'dev': create_console_handler,
    'prod': create_file_handler
}

handler_func = handler_funcs.get(app_env, create_console_handler)
handler = handler_func()

logger = logging.getLogger(app_name)
if not logger.handlers:
    # logger.addHandler(handler)
    thread_pool_handler = ThreadPoolHandler(handler)
    logger.addHandler(thread_pool_handler)
