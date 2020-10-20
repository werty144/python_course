class ContractError(Exception):
    """We use this error when someone breaks our contract."""


#: Special value, that indicates that validation for this type is not required.
Any = object


def validate_arg_types(arg_types, args):
    if arg_types is None:
        return True
    if len(arg_types) != len(args):
        return False
    bool_mask = map(lambda p: isinstance(p[0], p[1]), zip(args, arg_types))
    return all(bool_mask)


def validate_return_type(res, return_type):
    if return_type is None:
        return True
    return isinstance(res, return_type)


def contract(arg_types=None, return_type=None, raises=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not validate_arg_types(arg_types, args):
                raise ContractError()

            if raises is not None:
                try:
                    res = func(*args, **kwargs)
                except Exception as exc:
                    if type(exc) not in raises:
                        raise ContractError() from exc
                    raise exc
            else:
                res = func(*args, **kwargs)

            if not validate_return_type(res, return_type):
                raise ContractError()

            return res

        return wrapper
    return decorator
