"""
Example 2: Explorando la caché global de uv
Demuestra cómo uv reutiliza paquetes entre proyectos
"""
import subprocess
from pathlib import Path


def get_cache_info():
    """Obtiene información sobre la caché de uv."""
    print("📦 Información de la Caché Global de uv\n")
    
    # Directorio de caché
    result = subprocess.run(
        ["uv", "cache", "dir"],
        capture_output=True,
        text=True,
        check=True
    )
    cache_dir = Path(result.stdout.strip())
    print(f"📁 Ubicación: {cache_dir}")
    
    # Tamaño de caché si existe
    if cache_dir.exists():
        result = subprocess.run(
            ["du", "-sh", str(cache_dir)],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"💾 Tamaño: {size}")
    
    # Listar algunos paquetes en caché
    wheels_dir = cache_dir / "wheels-v1"
    if wheels_dir.exists():
        wheels = list(wheels_dir.rglob("*.whl"))[:10]
        if wheels:
            print(f"\n📚 Algunos paquetes en caché ({len(wheels)} mostrados):")
            for wheel in wheels:
                print(f"   • {wheel.name}")


def demonstrate_cache_reuse():
    """Demuestra la reutilización de caché entre proyectos."""
    print("\n" + "="*60)
    print("🔄 Demostración de Reutilización de Caché")
    print("="*60)
    
    projects = [
        Path("/tmp/uv_project_1"),
        Path("/tmp/uv_project_2"),
    ]
    
    # Limpiar proyectos anteriores
    for project in projects:
        if project.exists():
            subprocess.run(["rm", "-rf", str(project)], check=False)
        project.mkdir(parents=True)
    
    # Proyecto 1: Primera instalación (descarga)
    print("\n1️⃣  Proyecto 1: Primera instalación de requests")
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
    
    # Proyecto 2: Segunda instalación (desde caché)
    print("\n2️⃣  Proyecto 2: Instalación de requests (desde caché)")
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
    
    # Verificar instalación
    try:
        subprocess.run(["uv", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv is not installed.")
        exit(1)
    
    get_cache_info()
    show_pubgrub_example()
    
    print("\n" + "="*60)
    response = input("¿Demostrar reutilización de caché? (s/n): ")
    if response.lower() == 's':
        demonstrate_cache_reuse()
