#!/usr/bin/env python3
"""
Script to track learning progress in Python Engineering Labs.

Scans all my_solution/ folders for non-empty Python files
and generates a progress report that updates the main README.md.
"""

import re
from collections import defaultdict
from pathlib import Path


def count_non_empty_py_files(solution_dir: Path) -> bool:
    """Check whether there are non-empty Python files in the solution directory."""
    if not solution_dir.exists():
        return False

    for py_file in solution_dir.glob("*.py"):
        # Read file and verify it is not empty (ignoring comments and whitespace)
        content = py_file.read_text(encoding="utf-8")
        # Remove comments and whitespace
        code_lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if code_lines:
            return True
    return False


def scan_modules(base_path: Path) -> dict[str, dict[str, int]]:
    """
    Scan all modules and count completed topics.

    Returns:
        Dict with structure: {
            "module_name": {
                "completed": int,
                "total": int
            }
        }
    """
    progress = defaultdict(lambda: {"completed": 0, "total": 0})

    # Find all directories that are modules (start with a number)
    module_dirs = sorted([d for d in base_path.iterdir() if d.is_dir() and d.name[:2].isdigit()])

    for module_dir in module_dirs:
        module_name = module_dir.name

        # Find all subdirectories that are topics (have README.md)
        topics = []

        # For the design patterns module, search inside subcategories
        if "design_patterns" in module_name:
            for subcat_dir in module_dir.iterdir():
                if subcat_dir.is_dir():
                    topics.extend(
                        [
                            t
                            for t in subcat_dir.iterdir()
                            if t.is_dir() and (t / "README.md").exists()
                        ]
                    )
        else:
            topics = [t for t in module_dir.iterdir() if t.is_dir() and (t / "README.md").exists()]

        progress[module_name]["total"] = len(topics)

        # Check how many have solutions
        for topic_dir in topics:
            solution_dir = topic_dir / "my_solution"
            if count_non_empty_py_files(solution_dir):
                progress[module_name]["completed"] += 1

    return dict(progress)


def generate_progress_table(progress: dict[str, dict[str, int]]) -> str:
    """Generate a Markdown table with the progress."""
    lines = [
        "## My Learning Progress",
        "",
        "| Module | Completed | Total | Progress | Percentage |",
        "|--------|-----------|-------|----------|------------|",
    ]

    total_completed = 0
    total_topics = 0

    for module_name, stats in progress.items():
        completed = stats["completed"]
        total = stats["total"]
        total_completed += completed
        total_topics += total

        percentage = (completed / total * 100) if total > 0 else 0
        bar_length = 20
        filled = int(bar_length * completed / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        # Format module name (remove number prefix and underscores)
        display_name = re.sub(r"^\d+_", "", module_name).replace("_", " ").title()

        lines.append(
            f"| {display_name} | {completed} | {total} | {bar} | {percentage:.1f}% |"
        )

    # Add total row
    total_percentage = (total_completed / total_topics * 100) if total_topics > 0 else 0
    total_filled = int(20 * total_completed / total_topics) if total_topics > 0 else 0
    total_bar = "█" * total_filled + "░" * (20 - total_filled)

    lines.extend(
        [
            "|--------|-----------|-------|----------|------------|",
            f"| **TOTAL** | **{total_completed}** | **{total_topics}** | {total_bar} | **{total_percentage:.1f}%** |",
        ]
    )

    lines.append("")
    lines.append(f"*Last updated: {Path.cwd().name}*")
    lines.append("")

    return "\n".join(lines)


def update_readme(base_path: Path, progress_table: str) -> None:
    """Update the main README.md with the progress table."""
    readme_path = base_path / "README.md"

    if not readme_path.exists():
        print(f"⚠️  README.md not found at {base_path}")
        return

    content = readme_path.read_text(encoding="utf-8")

    # Find the progress section and replace it
    progress_section_pattern = r"## My Learning Progress.*?(?=\n## |\Z)"

    if re.search(progress_section_pattern, content, re.DOTALL):
        # Replace existing section
        new_content = re.sub(
            progress_section_pattern, progress_table.rstrip() + "\n\n", content, flags=re.DOTALL
        )
    else:
        # Append at the end
        new_content = content.rstrip() + "\n\n" + progress_table

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"✅ README.md updated at {readme_path}")


def main() -> None:
    """Main entry point."""
    base_path = Path(__file__).parent.parent

    print("🔍 Scanning modules and topics...")
    progress = scan_modules(base_path)

    print("📝 Generating progress table...")
    progress_table = generate_progress_table(progress)

    print("\n" + progress_table)

    print("\n💾 Updating README.md...")
    update_readme(base_path, progress_table)

    print("\n✨ Progress updated successfully!")


if __name__ == "__main__":
    main()
