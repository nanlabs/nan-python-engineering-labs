"""Working example of variables and data types."""

from typing import TypedDict


class Profile(TypedDict):
    """Typed structure for a simple profile."""

    name: str
    age: int
    active: bool
    skills: list[str]
    score: float


def build_profile(name: str, age: int, active: bool) -> Profile:
    """Build a simple profile using Python's basic data types."""
    return {
        "name": name,
        "age": age,
        "active": active,
        "skills": ["python", "testing", "automation"],
        "score": 9.5,
    }


def describe_profile(profile: Profile) -> str:
    """Summarize the profile contents and the values it stores."""
    skills = ", ".join(profile["skills"])
    return (
        f"{profile['name']} ({profile['age']} years old) | "
        f"active={profile['active']} | score={profile['score']} | skills={skills}"
    )


def main() -> None:
    profile = build_profile("Ada", 32, True)
    print(describe_profile(profile))
    print({key: type(value).__name__ for key, value in profile.items()})


if __name__ == "__main__":
    main()
