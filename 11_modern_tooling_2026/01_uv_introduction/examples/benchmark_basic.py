"""
Example 1: Benchmark básico pip vs uv
"""
import subprocess
import time
from pathlib import Path

def create_test_requirements():
    """Crea archivo requirements.txt de prueba."""
    requirements = [
        "requests==2.31.0",
        "pandas==2.2.0",
        "numpy==1.26.0",
        "flask==3.0.0",
        "pytest==8.0.0",
    ]
    
    req_file = Path("temp_requirements.txt")
    req_file.write_text("\n".join(requirements))
    return req_file

def benchmark_pip(requirements_file: Path) -> float:
    """Mide tiempo de instalación con pip."""
    # Crear venv temporal
    subprocess.run(["python", "-m", "venv", "temp_venv_pip"], check=True)
    
    pip_path = "temp_venv_pip/bin/pip"
    
    start = time.perf_counter()
    result = subprocess.run(
        [pip_path, "install", "-r", str(requirements_file)],
        capture_output=True,
        text=True
    )
    elapsed = time.perf_counter() - start
    
    # Cleanup
    subprocess.run(["rm", "-rf", "temp_venv_pip"], check=True)
    
    return elapsed

def benchmark_uv(requirements_file: Path) -> float:
    """Mide tiempo de instalación con uv."""
    # Crear venv con uv
    subprocess.run(["uv", "venv", "temp_venv_uv"], check=True)
    
    start = time.perf_counter()
    result = subprocess.run(
        ["uv", "pip", "install", "-r", str(requirements_file)],
        capture_output=True,
        text=True
    )
    elapsed = time.perf_counter() - start
    
    # Cleanup
    subprocess.run(["rm", "-rf", "temp_venv_uv"], check=True)
    
    return elapsed

if __name__ == "__main__":
    print("🚀 Benchmark: pip vs uv\n")
    
    req_file = create_test_requirements()
    print(f"📦 Instalando 5 paquetes populares...\n")
    
    print("⏱️  Midiendo pip...")
    pip_time = benchmark_pip(req_file)
    print(f"   pip: {pip_time:.2f}s\n")
    
    print("⏱️  Midiendo uv...")
    uv_time = benchmark_uv(req_file)
    print(f"   uv:  {uv_time:.2f}s\n")
    
    speedup = pip_time / uv_time
    print(f"✨ Speedup: {speedup:.1f}x más rápido con uv!")
    
    # Cleanup
    req_file.unlink()
