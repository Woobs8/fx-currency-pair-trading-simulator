
def parse_arg(arg, arg_name: str, type: type, required: bool = False):
    if arg is None:
        if required:
            raise ValueError("config error '{}': argument not specified".format(arg_name))
        elif type is bool:
            return False
        else:
            return arg
    else:
        try:
            return type(arg)
        except ValueError:
            raise ValueError("config error '{}': invalid value '{}'".format(arg_name, arg))