import importlib


def load_class(name):
    module_name, attribute = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def get_instance(path, **options):
    cls = load_class(path)
    return cls(**options)
