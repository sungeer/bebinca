from enum import Enum


class ErrorCode(Enum):
    # 参数错误 (模块代码 10)
    PARAMETER_MISSING = 10100  # '参数缺失'
    PARAMETER_FORMAT_ERROR = 10101  # '参数格式错误'
    REQUEST_DATA_ERROR = 10102  # '请求数据异常'

    # 权限相关错误 (模块代码 20)
    UNAUTHORIZED = 20100  # '未授权'
    FORBIDDEN = 20101  # '禁止访问'
    NOT_FOUND = 20102  # '未找到'

    # 用户相关错误 (模块代码 30)
    USER_NOT_FOUND = 30200  # '用户不存在'
    INCORRECT_PASSWORD = 30201  # '密码错误'

    # 数据库相关错误 (模块代码 40)
    DB_INSERT_FAILED = 40300  # '数据插入失败'
    DB_QUERY_FAILED = 40301  # '数据查询失败'

    # 外部服务错误 (模块代码 50)
    EXTERNAL_API_CALL_FAILED = 50400  # '第三方API调用失败'
    EXTERNAL_API_TIMEOUT = 50401  # '第三方API超时'
    EXTERNAL_API_MISSING_DATA = 50402  # '第三方API返回缺少data数据'

    # 序列化/反序列化错误 (模块代码 60)
    SERIALIZATION_FAILED = 60500  # '序列化失败'
    DESERIALIZATION_FAILED = 60501  # '反序列化失败'

    # 服务器相关错误 (模块代码 70)
    SERVER_ERROR = 70700  # '服务器异常'


if __name__ == '__main__':
    error_code = ErrorCode.PARAMETER_MISSING
    print(error_code.value)
