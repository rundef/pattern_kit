# pattern_kit

[![PyPI - Version](https://img.shields.io/pypi/v/pattern_kit)](https://pypi.org/project/pattern-kit/)
[![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)](https://pypi.org/project/pattern_kit)
[![CI](https://github.com/rundef/pattern_kit/actions/workflows/ci.yml/badge.svg)](https://github.com/rundef/pattern_kit/actions/workflows/ci.yml)
[![Documentation](https://app.readthedocs.org/projects/pattern-kit/badge/?version=latest)](https://pattern-kit.readthedocs.io/en/latest/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pattern_kit)](https://pypistats.org/packages/pattern-kit)


> A modern Python library of reusable software design patterns.  
> **Your blueprint for better Python architecture.**

---

`pattern_kit` is a developer-friendly Python library offering clean, idiomatic implementations of common software design patterns. It focuses on real-world usability, pragmatic APIs, and simple integration into your projects.

While many examples exist online, `pattern_kit` is designed as a pip-installable, production-grade package with a consistent structure and proper documentation - making design patterns approachable and usable in everyday codebases.

---

## Features

- Clean, idiomatic Python implementations
- Supports both synchronous and asynchronous designs
- Type-annotated and easy to extend
- Ready-to-use patterns for real-world projects
- [Extensive documentation with examples](https://pattern-kit.readthedocs.io/en/latest/)
- Zero dependencies - pure Python, clean and portable

---

## Installation

```bash
pip install pattern_kit
```

## Documentation

Full usage examples and pattern guides are available in the [official documentation](https://pattern-kit.readthedocs.io/en/latest/)

## Quick Examples

### Singleton example (using decorator)

```python
from pattern_kit import singleton

@singleton
class Config:
    def __init__(self, env="dev"):
        self.env = env

# you can also use this syntax:
#
# from pattern_kit import Singleton
# class Config(Singleton):
#     ...

cfg = Config(env="prod")
print(cfg.env)  # "prod"

same = Config()
assert same is cfg
```

### Event (multicast) example

```python
from pattern_kit import Event

def listener(msg):
    print(f"[sync] {msg}")

async def async_listener(msg):
    print(f"[async] {msg}")

on_message = Event()
on_message += listener
on_message += async_listener

on_message("hello!")         # fire-and-forget
await on_message.call_async("world")  # fully awaited
```

## Who is this for?

Python developers who want to structure their codebase better and apply solid, proven software architecture principles.

## Contributing

Contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests.
