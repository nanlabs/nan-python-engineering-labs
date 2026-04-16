"""
Example 2: Exploring the global uv cache
Demonstrates how uv reuses packages across projects
"""
import subprocess
from pathlib import Path


def get_cache_info():
    """Get information about the uv cache."""
    print("📦 uv Global Cache Information\n")
    
    # Cache directory
    result = subprocess.run(
        ["uv", "cache", "dir"],
        capture_output=True,
        text=True,
        check=True
    )
    cache_dir = Path(result.stdout.strip())
    print(f"📁 Location: {cache_dir}")
    
    # Cache size if it exists
    if cache_dir.exists():
        result = subprocess.run(
            ["du", "-sh", str(cache_dir)],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"💾 Size: {size}")
    
    # List some cached packages
    wheels_dir = cache_dir / "wheels-v1"
    if wheels_dir.exists():
        wheels = list(wheels_dir.rglob("*.whl"))[:10]
        if wheels:
            print(f"\n📚 Some cached packages in cache ({len(wheels)} shown):")
            for wheel in wheels:
                print(f"   • {wheel.name}")


def demonstrate_cache_reuse():
    """Demonstrate cache reuse across projects."""
    print("\n" + "="*60)
    print("🔄 Cache Reuse Demonstration")
    print("="*60)
    
    projects = [
        Path("/tmp/uv_project_1"),
        Path("/tmp/uv_project_2"),
    ]
    
    # Clean up previous projects
    for project in projects:
        if project.exists():
            subprocess.run(["rm", "-rf", str(project)], check=False)
        project.mkdir(parents=True)
    
    # Project 1: First installation (download)
    print("\n1️⃣  Project 1: First requests installation")
    subprocess.run(["uv", "venv", str(projects[0] / ".venv")], check=True)
    
    result = subprocess.run(
        ["uv", "pip", "install", 
         "--python", str(projects[0] / ".venv" / "bin" / "python"),
         "requests==2.31.0"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    
    # Project 2: Second installation (from cache)
    print("\n2️⃣  Project 2: Requests installation (from cache)")
    subprocess.run(["uv", "venv", str(projects[1] / ".venv")], check=True)
    
    result = subprocess.run(
        ["uv", "pip", "install",
         "--python", str(projects[1] / ".venv" / "bin" / "python"),
         "requests==2.31.0"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    
    print("\n✓ Note: The second installation is instant thanks to cache reuse")
    
    # Cleanup
    for project in projects:
        subprocess.run(["rm", "-rf", str(project)], check=False)


def show_pubgrub_example():
    """Show a conceptual example of the PubGrub algorithm."""
    print("\n" + "="*60)
    print("🧮 PubGrub Algorithm - Conceptual Example")
    print("="*60)
    
    print("""
PubGrub builds a decision graph incrementally:

Suppose we install a package with these dependencies:

    my-app
    ├── requests >=2.28.0
    └── flask >=2.0.0
        └── werkzeug >=2.0.0
            └── markupsafe >=2.0.0

Resolution Process (simplified):

1. Select: my-app (root)
2. Add: requests >=2.28.0 → select 2.31.0
3. Add: flask >=2.0.0 → select 3.0.0
4. Add: werkzeug >=2.0.0 (dependency of flask) → select 3.0.0
5. Add: markupsafe >=2.0.0 (dependency of werkzeug) → select 2.1.3

Advantages vs Backtracking (pip):
✓ Detects conflicts early
✓ Produces clearer error messages
✓ Avoids costly backtracking steps
✓ Faster on complex dependency graphs
""")


if __name__ == "__main__":
    print("🏗️  uv: Architecture and Cache\n")
    
    # Verify installation
    try:
        subprocess.run(["uv", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv is not installed.")
        exit(1)
    
    get_cache_info()
    show_pubgrub_example()
    
    print("\n" + "="*60)
    response = input("Demonstrate cache reuse? (y/n): ")
    if response.lower() == 'y':
        demonstrate_cache_reuse()
