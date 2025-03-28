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

## Quick Example

```python
from pattern_kit import Observable, Observer

class MyObserver(Observer):
    def notify(self, event, data=None):
        print(f"Received: {event} - {data}")

obs = Observable()
observer = MyObserver()

obs += observer
obs.notify("on_data", {"price": 42})
```

## Who is this for?

Python developers who want to structure their codebase better and apply solid, proven software architecture principles.

## Contributing

Contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests.
