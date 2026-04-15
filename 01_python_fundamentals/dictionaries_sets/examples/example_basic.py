"""Working example of dictionaries and sets."""


def count_statuses(statuses: list[str]) -> dict[str, int]:
    """Count occurrences with a dictionary."""
    result: dict[str, int] = {}
    for status in statuses:
        result[status] = result.get(status, 0) + 1
    return result


def unique_languages(teams: dict[str, set[str]]) -> set[str]:
    """Merge all languages declared by the teams."""
    languages: set[str] = set()
    for values in teams.values():
        languages.update(values)
    return languages


def main() -> None:
    print(count_statuses(["open", "done", "open", "review"]))
    print(unique_languages({"backend": {"python", "sql"}, "data": {"python", "rust"}}))


if __name__ == "__main__":
    main()
