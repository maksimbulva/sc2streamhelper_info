from django.utils.html import escape


class FetchFailedException(Exception):
    pass


class BadParameter(Exception):
    def __init__(self, parameter_name, parameter_value):
        self.parameter_name = escape(parameter_name)
        self.parameter_value = escape(parameter_value)


class BnetRequestFailed(Exception):
    def __init__(self, request_status_code):
        self.request_status_code = str(request_status_code)
