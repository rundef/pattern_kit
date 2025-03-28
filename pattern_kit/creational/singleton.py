class Singleton:
    """
    A basic singleton implementation via class-level instance storage.

    This is useful when you want to ensure only one instance of a class
    is ever created.
    """

    instances: dict[str, "Singleton"] = {}

    @classmethod
    def create(cls, *args, **kwargs) -> "Singleton":
        """
        Create and store a new singleton instance for this class.
        Overwrites any existing instance.
        """
        instance = cls(*args, **kwargs)
        cls.instances[cls.__name__] = instance
        return instance

    @classmethod
    def instance(cls, *args, **kwargs) -> "Singleton":
        """
        Retrieve the singleton instance for this class.
        If it doesn't exist, creates one using `create(**kwargs)`.
        """
        if cls.__name__ not in cls.instances:
            return cls.create(*args, **kwargs)
        return cls.instances[cls.__name__]

def singleton(cls):
    """
    A decorator that transforms a class into a singleton.
    """
    _instance = {}

    def get_instance(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return get_instance