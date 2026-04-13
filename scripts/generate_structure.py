#!/usr/bin/env python3
"""
Script to generate the basic module and topic structure.

Creates the folder structure and basic README files
for all modules of the Python Engineering Labs project.
"""

from pathlib import Path
from typing import Dict

# Definition of all modules and their topics
MODULES = {
    "01_python_fundamentals": {
        "description": "Python Fundamentals",
        "topics": [
            "variables_data_types_optional",
            "operators_expressions_optional",
            "control_structures",
            "lists_tuples",
            "dictionaries_sets",
            "basic_functions",
            "comprehensions",
            "advanced_strings",
            "input_output_optional",
            "module_imports",
            "basic_error_handling",
            "basic_debugging_optional",
        ],
    },
    "02_intermediate_python": {
        "description": "Intermediate Python",
        "topics": [
            "advanced_functions",
            "basic_decorators",
            "closures",
            "text_file_handling",
            "csv_json",
            "exception_handling",
            "basic_context_managers",
            "basic_iterators",
            "generators",
            "modules_packages",
            "pathlib",
            "datetime_time",
            "collections_module",
            "itertools",
            "regex_optional",
        ],
    },
    "03_basic_intermediate_oop": {
        "description": "Basic and Intermediate OOP",
        "topics": [
            "classes_objects",
            "attributes_methods",
            "init_self",
            "basic_inheritance",
            "multiple_inheritance",
            "polymorphism",
            "encapsulation",
            "special_methods",
            "properties",
            "basic_descriptors",
            "composition_vs_inheritance",
            "dataclasses_optional",
        ],
    },
    "05_modern_concurrency": {
        "description": "Modern Concurrency and Parallelism",
        "topics": [
            "concurrency_models",
            "basic_threading",
            "threading_freethreading",
            "thread_pools",
            "locks_semaphores",
            "barriers_events",
            "subinterpreters_usage",
            "subinterpreters_communication",
            "basic_multiprocessing",
            "shared_memory",
            "process_pools",
            "asyncio_fundamentals",
            "event_loop_internals",
            "coroutines_async_await",
            "asyncio_patterns",
            "taskgroups",
            "asyncio_streams",
            "aiohttp_httpx",
            "asyncio_debugging",
            "producer_consumer",
            "parallel_pipeline",
            "map_reduce",
            "actor_model",
            "race_detection",
            "profiling_concurrent",
        ],
    },
    "06_typing_metaprogramming": {
        "description": "Static Typing and Metaprogramming",
        "topics": [
            "basic_type_hints",
            "advanced_typing",
            "generics_typevar",
            "protocol_structural_typing",
            "typeddict_namedtuple",
            "union_optional",
            "literal_types",
            "overload",
            "basic_mypy",
            "runtime_type_checking",
            "metaclasses_intro",
            "advanced_metaclasses",
            "init_subclass",
            "set_name_descriptor",
            "advanced_descriptors",
            "abstract_base_classes",
            "class_decorators",
            "dynamic_classes",
            "introspection_inspect",
            "ast_basics",
            "ast_manipulation",
            "exec_eval_compile",
        ],
    },
    "08_application_architecture": {
        "description": "Application Architecture",
        "topics": [
            "solid_principles",
            "single_responsibility",
            "open_closed",
            "liskov_substitution",
            "interface_segregation",
            "dependency_inversion",
            "dependency_injection",
            "inversion_control",
            "ddd_intro",
            "entities_value_objects",
            "repositories",
            "services_uow",
            "hexagonal_architecture",
            "ports_adapters",
            "event_driven_arch",
            "cqrs_pattern",
            "structured_logging",
            "observability",
        ],
    },
    "09_testing_qa": {
        "description": "Testing and Quality Assurance",
        "topics": [
            "pytest_fundamentals",
            "fixtures",
            "parametrize",
            "mocking_unittest",
            "pytest_mock",
            "coverage_analysis",
            "hypothesis_intro",
            "property_based_testing",
            "mutation_testing",
            "pytest_asyncio",
            "integration_testing",
            "contract_testing",
            "tdd_basics",
            "bdd_behave_optional",
            "test_organization",
            "ci_testing",
        ],
    },
    "10_performance_optimization": {
        "description": "Performance and Optimization",
        "topics": [
            "profiling_cprofile",
            "line_profiler",
            "pyspy_profiling",
            "benchmarking_timeit",
            "pytest_benchmark",
            "optimization_techniques",
            "cython_basics",
            "numpy_vectorization",
            "numba_jit",
            "pypy_intro",
            "lazy_evaluation",
            "caching_lru",
            "memory_optimization",
            "algorithmic_complexity",
        ],
    },
    "12_fastapi_complete": {
        "description": "FastAPI Complete",
        "topics": [
            "fastapi_intro",
            "routing",
            "path_query_params",
            "request_body",
            "pydantic_models",
            "dependency_injection",
            "response_models",
            "file_uploads",
            "background_tasks",
            "websockets",
            "middleware",
            "cors",
            "authentication_jwt",
            "oauth2",
            "security_best_practices",
            "openapi_customization",
            "testing_fastapi",
            "sqlalchemy_integration",
            "async_databases",
            "alembic_migrations",
            "fastapi_performance",
            "uvicorn_gunicorn",
            "rate_limiting",
            "redis_caching",
            "logging_monitoring",
            "error_handling",
            "graphql_optional",
            "deployment",
        ],
    },
    "13_backend_ecosystem": {
        "description": "Modern Backend Ecosystem",
        "topics": [
            "sqlalchemy_2_intro",
            "sqlalchemy_async",
            "postgresql_advanced",
            "redis_basics",
            "redis_patterns",
            "redis_pubsub",
            "rabbitmq_basics",
            "kafka_basics",
            "celery_intro",
            "arq_async_tasks",
            "grpc_intro",
            "protobuf",
            "rest_api_design",
            "api_versioning",
            "configuration_management",
            "structured_logging",
            "opentelemetry",
            "prometheus_metrics",
            "elasticsearch_optional",
            "graphql_schemas_optional",
        ],
    },
    "15_basic_data_science": {
        "description": "Basic Data Science",
        "topics": [
            "numpy_basics",
            "pandas_intro",
            "pandas_operations",
            "matplotlib_basics",
            "seaborn_viz",
            "data_cleaning",
            "exploratory_analysis",
            "jupyter_notebooks_optional",
            "pandas_performance",
            "polars_intro",
        ],
    },
}


def create_topic_structure(base_path: Path, topic_name: str) -> None:
    """Create the folder structure for a topic."""
    topic_path = base_path / topic_name
    topic_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (topic_path / "examples").mkdir(exist_ok=True)
    (topic_path / "exercises").mkdir(exist_ok=True)
    (topic_path / "tests").mkdir(exist_ok=True)
    (topic_path / "my_solution").mkdir(exist_ok=True)
    (topic_path / "references").mkdir(exist_ok=True)

    # Create basic README
    readme_content = f"""# {topic_name.replace("_", " ").title()}

⏱️ **Estimated time: 2-3 hours**

## 1. Definition

*[To complete: 200-300 words explaining the concept technically]*

## 2. Practical Application

### Use Cases

1. **Case 1**:
2. **Case 2**:
3. **Case 3**:

### Code Example

```python
# TODO: Add example
```

## 3. Why Is It Important?

*[To complete: Problem it solves, history, inspiration]*

## 4. References

- [Official Python documentation](https://docs.python.org/)
- [Relevant PEP]()
- [Technical article]()

## 5. Practice Task

### Basic Level
*[To complete]*

### Intermediate Level
*[To complete]*

### Advanced Level
*[To complete]*

## 6. Summary

- Key point 1
- Key point 2
- Key point 3

## 7. My Personal Analysis

> ✍️ **Space for your reflection**
>
> Write your observations, questions, and conclusions after completing this topic...
"""

    readme_path = topic_path / "README.md"
    if not readme_path.exists():
        readme_path.write_text(readme_content)

    # Create basic references file
    links_content = f"""# References: {topic_name.replace("_", " ").title()}

## Official Documentation
- [Python Docs](https://docs.python.org/)

## Articles
- *[To be added]*

## Videos
- *[To be added]*

## Example Repositories
- *[To be added]*
"""

    links_path = topic_path / "references" / "links.md"
    if not links_path.exists():
        links_path.write_text(links_content)


def create_module(base_path: Path, module_name: str, module_info: Dict) -> None:
    """Create the complete structure of a module."""
    module_path = base_path / module_name
    module_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Creating module: {module_name}")

    # Create module README
    readme_content = f"""# Module: {module_info["description"]}

## Description

*[To complete: General description of the module]*

## Learning Objectives

- Objective 1
- Objective 2
- Objective 3

## Contents ({len(module_info["topics"])} Topics)

"""

    for i, topic in enumerate(module_info["topics"], 1):
        topic_title = topic.replace("_", " ").title()
        readme_content += f"{i}. [{topic_title}]({topic}/)\n"

    readme_content += f"""
## Total Estimated Time

**{len(module_info["topics"]) * 2}-{len(module_info["topics"]) * 3} hours**

## Recommended Order

Follow the numerical order for a logical progression.
"""

    readme_path = module_path / "README.md"
    if not readme_path.exists():
        readme_path.write_text(readme_content)

    # Create each topic
    for topic in module_info["topics"]:
        create_topic_structure(module_path, topic)
        print(f"  ✓ {topic}")


def main() -> None:
    """Generate the complete project structure."""
    base_path = Path(__file__).parent.parent

    print("🚀 Generating module structure...")
    print()

    for module_name, module_info in MODULES.items():
        create_module(base_path, module_name, module_info)
        print()

    print("✅ Structure generated successfully!")
    print()
    print("📝 Next steps:")
    print("   1. Review the created modules")
    print("   2. Populate the READMEs with content")
    print("   3. Add examples and exercises")
    print("   4. Run: uv run scripts/progress.py")


if __name__ == "__main__":
    main()
