"""
Example: installation and verification of uv in different environments
"""

import platform
import subprocess
import sys
from pathlib import Path


def check_uv_installation():
    """Verify whether uv is installed correctly."""
    print("🔍 Checking uv installation\n")

    try:
        # Version
        result = subprocess.run(["uv", "version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"✅ uv installed: {version}")

        # Location
        result = subprocess.run(["which", "uv"], capture_output=True, text=True, check=True)
        location = result.stdout.strip()
        print(f"📍 Location: {location}")

        # Binary size
        size_mb = Path(location).stat().st_size / (1024 * 1024)
        print(f"💾 Size: {size_mb:.2f} MB")

        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv is not installed")
        return False


def show_system_info():
    """Show system information."""
    print("\n📊 System Information")
    print(f"{'=' * 50}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"{'=' * 50}\n")


def show_configuration():
    """Show the current uv configuration."""
    print("⚙️  uv configuration\n")

    # Cache directory
    try:
        result = subprocess.run(["uv", "cache", "dir"], capture_output=True, text=True, check=True)
        cache_dir = Path(result.stdout.strip())
        print(f"📁 Cache directory: {cache_dir}")

        if cache_dir.exists():
            # Cache size
            result = subprocess.run(
                ["du", "-sh", str(cache_dir)], capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                print(f"💾 Cache size: {size}")
        else:
            print("   (Cache does not exist yet)")

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error getting configuration: {e}")

    # Relevant environment variables
    print("\n🔧 Relevant Environment Variables:")
    env_vars = [
        "UV_CACHE_DIR",
        "UV_INDEX_URL",
        "UV_VERBOSE",
        "UV_HTTP_TIMEOUT",
    ]

    import os

    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   {var}={value}")
        else:
            print(f"   {var}=(not configured)")


def show_available_commands():
    """List available uv commands."""
    print("\n📚 Available Commands\n")

    result = subprocess.run(["uv", "--help"], capture_output=True, text=True, check=True)

    # Parse commands
    lines = result.stdout.split("\n")
    in_commands = False

    for line in lines:
        if "Commands:" in line:
            in_commands = True
            continue

        if in_commands and line.strip():
            if line.startswith("  ") and not line.startswith("   "):
                # This is a command
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    cmd, desc = parts
                    print(f"   • {cmd:12} {desc}")
            elif not line.startswith("  "):
                break


def demonstrate_config_file():
    """Demonstrate creating a configuration file."""
    print("\n📝 Example Configuration File\n")

    config_content = """
# .uv/config.toml - Project local configuration

[tool.uv]
# Main package index
index-url = "https://pypi.org/simple"

# Additional indexes (for example, private indexes)
# extra-index-url = ["https://private.pypi.org/simple"]

[tool.uv.pip]
# Do not use prebuilt binaries for these packages
# no-binary = ["scipy"]

# Use wheels only (do not compile from source)
# only-binary = [":all:"]

[tool.uv.resolution]
# Do not allow pre-releases
prerelease = "disallow"

# Resolution strategy
# resolution = "highest"  # or "lowest" or "lowest-direct"
"""

    print(config_content)

    # Ask whether to create the file
    response = input("Create this file in the current directory? (y/n): ")
    if response.lower() == "y":
        config_path = Path.cwd() / ".uv" / "config.toml"
        config_path.parent.mkdir(exist_ok=True)
        config_path.write_text(config_content.strip())
        print(f"✅ File created at: {config_path}")


if __name__ == "__main__":
    print("🚀 uv: Installation and Configuration\n")

    show_system_info()

    if not check_uv_installation():
        print("\n💡 To install uv, run:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)

    show_configuration()
    show_available_commands()
    demonstrate_config_file()

    print("\n✨ Configuration complete!")
