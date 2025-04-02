import importlib
from typing import Any, Union
from pattern_kit import ServiceLocator

def resolve_class(class_name: str, class_map: dict[str, type] = None) -> type:
    """
    Resolve a class either from a provided class map or by importing a dotted path.

    Args:
        class_name (str): The class name or full import path.
        class_map (dict[str, type], optional): A dictionary of available classes by name.

    Returns:
        type: The resolved class object.

    Raises:
        ValueError: If the class cannot be resolved from the map or path.
    """
    if class_map and class_name in class_map:
        return class_map[class_name]
    if "." not in class_name:
        raise ValueError(f"Unknown class '{class_name}', and no dotted path provided.")
    module_path, _, cls_name = class_name.rpartition(".")
    module = importlib.import_module(module_path)
    return getattr(module, cls_name)


def build_object(cfg: dict[str, Any], class_map: dict[str, type] = None) -> Any:
    """
    Instantiate an object from a config dict with 'class' and optional 'args'.

    Args:
        cfg (dict): Must contain 'class' and optionally 'args'.
        class_map (dict[str, type], optional): Safe list of allowed classes.

    Returns:
        Any: Instantiated object.
    """
    cls_name = cfg["class"]
    args = cfg.get("args", {})
    cls = resolve_class(cls_name, class_map)
    return cls(**args)


def build_from_config(
    config: dict[str, Union[dict, list]],
    class_map: dict[str, type] = None,
    register: bool = False,
    register_raw: bool = False
) -> dict[str, Any]:
    """
    Build one or more objects from a config dictionary.

    Supports both object configs (with 'class' + optional 'args')
    and raw config entries (passed through as-is).

    Args:
        config (dict): The full config mapping keys to:
                       - object configs (dict with 'class')
                       - lists of object configs
                       - raw values (passed through)
        class_map (dict[str, type], optional): Optional map of allowed classes.
        register (bool): If True, registers each built object with ServiceLocator[key].
        register_raw (bool): If True, also register raw (non-built) values in the ServiceLocator.

    Returns:
        dict[str, Any]: Dictionary of created or passed-through values by key.
    """
    result = {}
    for key, entry in config.items():
        if isinstance(entry, dict) and "class" in entry:
            result[key] = build_object(entry, class_map)
        elif isinstance(entry, list) and all(isinstance(e, dict) and "class" in e for e in entry):
            result[key] = [build_object(e, class_map) for e in entry]
        else:
            result[key] = entry
            if not register_raw:
                continue

        if register:
            ServiceLocator.register(key, result[key])

    return result
