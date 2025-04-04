Strategy Pattern
================

The **Strategy pattern** defines a family of interchangeable algorithms or behaviors, encapsulates each one, and allows them to be swapped at runtime without modifying the calling code.

This pattern is useful when multiple approaches exist to perform a task, and you want to select the appropriate one dynamically, promoting cleaner logic and improved maintainability.

This pattern should be implemented manually: it does not require built-in helpers from `pattern_kit`.

Use Cases
---------

- Switching between different sorting or filtering strategies
- Applying different pricing, tax, or discount rules
- Customizing logging, serialization, or validation logic
- Pluggable behavior in UI elements or background tasks
- AI/game agents choosing a decision-making strategy

Example
-------

.. code-block:: python

    from abc import ABC, abstractmethod

    class DiscountStrategy(ABC):
        @abstractmethod
        def apply(self, price: float) -> float:
            pass

    class NoDiscount(DiscountStrategy):
        def apply(self, price):
            return price

    class TenPercentOff(DiscountStrategy):
        def apply(self, price):
            return price * 0.9

    # Usage
    def calculate_total(price: float, strategy: DiscountStrategy) -> float:
        return strategy.apply(price)

    print(calculate_total(100, NoDiscount()))       # 100.0
    print(calculate_total(100, TenPercentOff()))    # 90.0

Benefits
--------

- Eliminates long if/else blocks
- Makes algorithms testable in isolation
- Allows behavior to change at runtime
- Encourages composition over inheritance

