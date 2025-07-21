def print_dict_recursive(obj, indent=1):
    if not hasattr(obj, "__dict__"):
        print("  " * indent + repr(obj))
        return
    for key, value in obj.__dict__.items():
        print("  " * indent + f"{key}: ", end="")
        if hasattr(value, "__dict__"):
            print()
            print_dict_recursive(value, indent + 1)
        elif isinstance(value, dict):
            print()
            print_dict_recursive_dict(value, indent + 1)
        else:
            print(repr(value))


def print_dict_recursive_dict(d: dict, indent=0):
    for k, v in d.items():
        print("  " * indent + f"{k}: ", end="")
        if hasattr(v, "__dict__"):
            print()
            print_dict_recursive(v, indent + 1)
        elif isinstance(v, dict):
            print()
            print_dict_recursive_dict(v, indent + 1)
        else:
            print(repr(v))
