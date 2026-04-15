"""
Example 1: Speed comparison between pip and uv
Demuestra la diferencia de rendimiento en operaciones comunes
"""
import subprocess
import time
from pathlib import Path


def measure_command(cmd: list[str], description: str) -> float:
    """Measure command execution time."""
    print(f"\n{'='*60}")
    print(f"Ejecutando: {description}")
    print(f"Comando: {' '.join(cmd)}")
    print('='*60)
    
    start = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False
    )
    elapsed = time.time() - start
    
    print(f"✓ Completed in {elapsed:.2f} seconds")
    if result.returncode != 0:
        print(f"⚠️  Error: {result.stderr[:200]}")
    
    return elapsed


def compare_installation():
    """Compare installation speed between pip and uv."""
    print("🔬 Benchmark: pip vs uv - installing requests")
    
    # Crear directorios temporales
    pip_venv = Path("/tmp/pip_test_venv")
    uv_venv = Path("/tmp/uv_test_venv")
    
    # Limpiar si existen
    for venv in [pip_venv, uv_venv]:
        if venv.exists():
            subprocess.run(["rm", "-rf", str(venv)], check=True)
    
    # Test con pip (tradicional)
    pip_time = 0
    pip_time += measure_command(
        ["python", "-m", "venv", str(pip_venv)],
        "pip: crear entorno virtual"
    )
    pip_time += measure_command(
        [str(pip_venv / "bin" / "pip"), "install", "requests"],
        "pip: install requests"
    )
    
    # Test con uv
    uv_time = 0
    uv_time += measure_command(
        ["uv", "venv", str(uv_venv)],
        "uv: crear entorno virtual"
    )
    uv_time += measure_command(
        ["uv", "pip", "install", "--python", str(uv_venv / "bin" / "python"), "requests"],
        "uv: install requests"
    )
    
    # Resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS")
    print("="*60)
    print(f"pip: {pip_time:.2f} seconds")
    print(f"uv:  {uv_time:.2f} seconds")
    print(f"uv es {pip_time/uv_time:.1f}x más rápido")
    print("="*60)
    
    # Cleanup
    subprocess.run(["rm", "-rf", str(pip_venv), str(uv_venv)], check=False)


def show_architecture():
    """Show information about uv architecture."""
    print("\n🏗️  uv architecture\n")
    
    # Versión
    result = subprocess.run(
        ["uv", "version"],
        capture_output=True,
        text=True,
        check=True
    )
    print(f"Versión: {result.stdout.strip()}")
    
    # Cache location
    result = subprocess.run(
        ["uv", "cache", "dir"],
        capture_output=True,
        text=True,
        check=True
    )
    print(f"Cache directory: {result.stdout.strip()}")
    
    # Cache size
    result = subprocess.run(
        ["uv", "cache", "prune", "--dry-run"],
        capture_output=True,
        text=True,
        check=False
    )
    print(f"\nInformación de caché:")
    print(result.stdout if result.returncode == 0 else "No hay caché")


if __name__ == "__main__":
    print("🚀 uv: Introduction and Architecture - Practical Examples\n")
    
    # Verificar que uv está instalado
    try:
        subprocess.run(["uv", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv no está instalado. Instálalo con:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        exit(1)
    
    show_architecture()
    
    # Preguntar si ejecutar benchmark
    print("\n" + "="*60)
    response = input("Run speed benchmark? (y/n): ")
    if response.lower() == 's':
        compare_installation()
    else:
        print("Benchmark omitido.")
