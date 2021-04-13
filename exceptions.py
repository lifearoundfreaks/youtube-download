class BaseBotException(Exception):
    pass


class InputValidationException(BaseBotException):
    """ User sent us invalid data """


class ForbiddenUserOperation(BaseBotException):
    """ User tries to do something we do not allow """
