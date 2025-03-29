import re

class DelegateMixin:
    def _delegate_methods(self, target, namespace=None, exclude=None, include=None, overwrite=False):
        """
        Dynamically delegates public methods from `target` to `self`.

        Args:
            target (object): The object whose methods to delegate.
            namespace (str, optional): If given, prepends this string to all delegated method names.
            exclude (list[str], optional): Regex patterns to skip. Defaults to ["_.*"] to skip private methods.
            include (list[str], optional): Regex patterns to include. If provided, only methods matching these are delegated.
            overwrite (bool, optional): If False (default), skip delegation if the method already exists on self.

        Notes:
            - Exclude patterns are applied before include patterns.
            - Only callable attributes are delegated.
        """
        exclude = exclude or [r"_.*"]
        include = include or []

        def matches(patterns, name):
            return any(re.match(p, name) for p in patterns)

        for name in dir(target):
            if exclude and matches(exclude, name):
                continue
            if include and not matches(include, name):
                continue

            method = getattr(target, name)
            if callable(method):
                delegated_name = f"{namespace}_{name}" if namespace else name
                if not overwrite and hasattr(self, delegated_name):
                    continue
                setattr(self, delegated_name, method)