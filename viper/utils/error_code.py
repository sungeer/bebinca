from enum import Enum


class ErrorCode(Enum):
    # 通用错误 (模块代码 10)
    PARAMETER_MISSING = 10100  # '参数缺失'
    PARAMETER_FORMAT_ERROR = 10101  # '参数格式错误'
    UNAUTHORIZED = 10102  # '未授权'
    FORBIDDEN = 10103  # '禁止访问'
    NOT_FOUND = 10104  # '未找到'

    # 用户相关错误 (模块代码 20)
    USER_NOT_FOUND = 20200  # '用户不存在'
    INCORRECT_PASSWORD = 20201  # '密码错误'

    # 数据库相关错误 (模块代码 30)
    DB_INSERT_FAILED = 30300  # '数据插入失败'
    DB_QUERY_FAILED = 30301  # '数据查询失败'

    # 外部服务错误 (模块代码 40)
    EXTERNAL_API_CALL_FAILED = 40400  # '第三方API调用失败'
    EXTERNAL_API_TIMEOUT = 40401  # '第三方API超时'
    EXTERNAL_API_MISSING_DATA = 40402  # '第三方API返回缺少data数据'

    # 序列化/反序列化错误 (模块代码 50)
    SERIALIZATION_FAILED = 50500  # '序列化失败'
    DESERIALIZATION_FAILED = 50501  # '反序列化失败'


if __name__ == '__main__':
    error_code = ErrorCode.PARAMETER_MISSING
    print(error_code.value)
