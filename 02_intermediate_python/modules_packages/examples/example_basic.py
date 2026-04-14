"""Working example of modules and packages."""

from importlib import import_module


def load_serializer(module_name: str):
    """Import a module dynamically and return it."""
    return import_module(module_name)


def main() -> None:
    json_module = load_serializer('json')
    print(json_module.dumps({'topic': 'modules', 'status': 'ready'}))


if __name__ == '__main__':
    main()
