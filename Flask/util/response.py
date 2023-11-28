def response(status_code: int, msg : str = None, data: dict = None, custom: list = []):

    response_format = {
        'success': True if status_code in range(200, 299) else False,
    }

    if isinstance(data, list) or isinstance(data, dict):
        response_format['data'] = data

    if msg :
        response_format['message'] = msg
        
    if custom :
        for key, value in custom:
            response_format[key] = value

    return response_format, status_code