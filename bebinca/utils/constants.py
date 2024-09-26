from bebinca.utils.error_enum import ErrorEnum

http_map = {
    400: 'Invalid request.',
    403: 'Access forbidden.',
    404: 'The requested URL was not found on the server.',
    405: 'The method is not allowed for the requested URL.'
}

error_map = {
    400: ErrorEnum.INVALID_REQUEST,
    403: ErrorEnum.FORBIDDEN,
    404: ErrorEnum.NOT_FOUND,
    405: ErrorEnum.METHOD_NOT_ALLOWED
}
