"""Implementation of contract decorator for hw3."""


class ContractError(Exception):
    """We use this error when someone breaks our contract."""


#: Special value, that indicates that validation for this type is not required.
Any = object


def check_isinstance(value_type_pair):
    """
    Check if first element of pair is type second element.

    Args:
        value_type_pair: Pair of value and type.

    Returns:
        True if isinstance, False otherwise.
    """
    return isinstance(value_type_pair[0], value_type_pair[1])


def validate_arg_types(arg_types, args):
    """
    Validate if args correspond to given types.

    If arg_types is None, returns True.

    Args:
        arg_types: wanted argument types
        args: arguments

    Returns:
        True if args correspond, False otherwise
    """
    if arg_types is None:
        return True
    if len(arg_types) != len(args):
        return False
    bool_mask = map(check_isinstance, zip(args, arg_types))
    return all(bool_mask)


def validate_return_type(res, return_type):
    """
    Check if res has given type.

    Returns True if return type is None.

    Args:
        res: Value to check type.
        return_type: Type to compare with.

    Returns:
        True if res has return_type False otherwise.
    """
    if return_type is None:
        return True
    return isinstance(res, return_type)


def exc_allowed(exc, allow_types):
    """
    Check if exception type is allowed.

    Args:
        exc: Exception.
        allow_types: Allowed exception types.

    Returns:
        True if allowed, False otherwise.
    """
    is_allowed = False
    for allowed in allow_types:
        if isinstance(exc, allowed):
            is_allowed = True
    return is_allowed


def validate_raises(func, raises, *args, **kwargs):
    """
    Validate if function raises allowed exception.

    If raises is None, no validation would be performed.

    Args:
        func: Function to evaluate.
        raises: Allowed exception types.
        args: Args to pass to function.
        kwargs: Kwargs to pass to function.

    Raises:
        ContractError: If raises check did not pass.
        Exception: Reraises the function exception.

    Returns:
        Returned function value, if evaluated successfully.
    """
    if raises is not None:
        try:
            res = func(*args, **kwargs)
        except Exception as exc:
            if not exc_allowed(exc, raises):
                raise ContractError() from exc
            raise exc
    else:
        res = func(*args, **kwargs)
    return res


def contract(arg_types=None, return_type=None, raises=None):
    """
    Make function decorator which checks argument types, return type and raised exceptions.

    Args:
        arg_types: Arguments types to check. If None, no check is performed.
        return_type: Return type to check. If None, no check is performed.
        raises: Exceptions that function can raise. If None, no check is performed.

    Raises:
        ContractError: If either arg_types, return_type or raises check did not pass.

    Returns:
        Decorator.
    """  # noqa:  E501
    def decorator(func):
        def wrapper(*args, **kwargs):  # noqa: WPS430
            if not validate_arg_types(arg_types, args):
                raise ContractError()

            res = validate_raises(func, raises, *args, **kwargs)

            if not validate_return_type(res, return_type):
                raise ContractError()

            return res

        return wrapper
    return decorator
