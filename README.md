# pattern_kit

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
- [Sphinx-based documentation with examples and guides](https://pattern-kit.readthedocs.io)

---

## Installation

```bash
pip install pattern_kit
```

## Quick Example

```
from pattern_kit.behavioral.observer import Observable, Observer

class MyObserver(Observer):
    def notify(self, event, data=None):
        print(f"Received: {event} — {data}")


obs = Observable()
observer = MyObserver()

obs += observer
obs.notify("on_data", {"price": 42})
```

## Documentation

Full usage examples and pattern guides are available in the official documentation: https://pattern-kit.readthedocs.io

## Patterns Included

- Behavioral:

  - Observer

  - EventEmitter

  - Strategy

- Creational:

  - Singleton

- Structural:

  - Decorator

More patterns will be added gradually with a focus on quality and documentation.

## Who is this for?

Python developers who want to structure their codebase better and apply solid, proven software architecture principles.

## Contributing

Contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests.

## License

MIT License — see LICENSE file.