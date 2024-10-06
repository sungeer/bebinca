import traceback

from viper.models.base_model import BaseModel
from viper.utils import tools
from viper.utils.decorators import log4p


class LogModel(BaseModel):

    def add_log(self, level, message):
        sql_str = '''
            INSERT INTO 
                logs 
                (Level, Message, CreatedTime) 
            VALUES 
                (%s, %s, %s)
        '''
        created_at = tools.current_time()
        self.conn()
        self.execute(sql_str, (level, message, created_at))
        self.commit()
        lastrowid = self.cursor.lastrowid
        self.close()
        return lastrowid

    @log4p('debug')
    def debug(self, message):  # 调试
        return self.add_log('DEBUG', message)

    @log4p('info')
    def info(self, message):
        return self.add_log('INFO', message)

    @log4p('warning')
    def warning(self, message):  # 警告 需要注意
        return self.add_log('WARNING', message)

    @log4p('error')
    def error(self, message, exc_info=None):  # 错误 需要立即处理
        if exc_info:
            tb_str = ''.join(traceback.format_exception(None, exc_info, exc_info.__traceback__))
            message = f'{message}\n{tb_str}'
        return self.add_log('ERROR', message)

    @log4p('critical')
    def critical(self, message):  # 严重错误 可能导致程序终止
        return self.add_log('CRITICAL', message)

    @log4p('notset')
    def notset(self, message):  # 未设置级别 用于初始化日志记录器
        return self.add_log('NOTSET', message)

    @log4p('exception')
    def exception(self, error):  # 用于捕获异常并记录堆栈信息
        tb_str = ''.join(traceback.format_exception(None, error, error.__traceback__))
        return self.add_log('ERROR', tb_str)


if __name__ == '__main__':
    try:
        pass
    except Exception as exc:
        LogModel().error(f'websocket error occurred: {exc}', exc_info=exc)  # exc_info=True
