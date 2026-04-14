# Module 04 - Advanced CPython Internals

## Overview

This module explores advanced CPython internals with a focus on the GIL evolution, free-threading (PEP 703), subinterpreters (PEP 684), memory management, and thread-safety techniques.

## Learning Objectives

- Understand historical design decisions around the GIL
- Learn the architecture and tradeoffs of optional-GIL Python builds
- Work with concepts related to subinterpreters and memory isolation
- Apply practical strategies for synchronization and race prevention
- Analyze object and memory internals in CPython

## Contents

1. [History of the Global Interpreter Lock](01_gil_history/)
2. [Limitations of the Traditional GIL](02_gil_limitations/)
3. [PEP 703 and Free-Threading in Python 3.13+](03_pep_703_free_threading/)
4. [Activating Free-Threading Builds](04_free_threading_activation/)
5. [GIL-Free Internal Architecture](05_gil_free_architecture/)
6. [Biased Reference Counting](06_biased_reference_counting/)
7. [Thread-Safe Garbage Collection](07_gc_thread_safe/)
8. [Performance Benchmarks: GIL vs No-GIL](08_performance_benchmarks/)
9. [C Extension Compatibility](09_c_extensions_compatibility/)
10. [Subinterpreters Introduction](10_subinterpreters_intro/)
11. [C API for Subinterpreters](11_api_c_subinterpreters/)
12. [Python API for Subinterpreters](12_api_python_subinterpreters/)
13. [Per-Interpreter GIL vs No-GIL](13_per_interpreter_gil/)
14. [Memory Isolation Between Interpreters](14_memory_isolation/)
15. [Communication Channels](15_communication_channels/)
16. [Atomic Operations](16_atomic_operations/)
17. [Data Races and Race Conditions](17_data_races/)
18. [Locks and Synchronization](18_locks_synchronization/)
19. [Thread-Local Storage](19_threading_local/)
20. [Thread-Safe Data Structures](20_thread_safe_structures/)
21. [PyObject Internal Structure](21_pyobject_structure/)
22. [Advanced Reference Counting](22_reference_counting/)
23. [Immortal Objects (PEP 683)](23_immortal_objects/)
24. [Caching and Interning](24_caching_interning/)
25. [Memory Layout and Compaction](25_memory_layout/)
26. [Migration Strategies](26_migration_strategies/)
27. [Thread-Safety Testing](27_testing_thread_safety/)

## Estimated Time

**80-110 hours**

## Main References

- [PEP 703 – Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [PEP 684 – A Per-Interpreter GIL](https://peps.python.org/pep-0684/)
- [PEP 683 – Immortal Objects](https://peps.python.org/pep-0683/)
- [Python Free-Threading HOWTO](https://docs.python.org/3/howto/free-threading-python.html)
