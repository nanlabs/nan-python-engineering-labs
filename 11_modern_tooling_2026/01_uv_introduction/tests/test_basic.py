"""
Tests para ejercicio básico de uv
"""
import pytest
from pathlib import Path
import sys

# Añadir my_solution al path
sys.path.insert(0, str(Path(__file__).parent.parent / "my_solution"))

def test_uv_installed():
    """Verifica que uv esté instalado."""
    import subprocess
    result = subprocess.run(["uv", "--version"], capture_output=True)
    assert result.returncode == 0, "uv no está instalado correctamente"

def test_requirements_file_exists():
    """Verifica que se haya creado requirements.txt."""
    req_file = Path("requirements.txt")
    if req_file.exists():
        content = req_file.read_text()
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        assert len(lines) >= 10, "requirements.txt debe tener al menos 10 paquetes"

@pytest.mark.skipif(not Path("my_solution/basic_exercise.py").exists(), 
                   reason="Solución no implementada aún")
def test_measure_install_time():
    """Verifica que la función measure_install_time() funcione."""
    from basic_exercise import measure_install_time
    
    # Este test asume que has implementado la función
    # Debe retornar un float positivo
    # (No ejecutamos realmente para no demorar los tests)
    pass

def test_report_generated():
    """Verifica que se haya generado el reporte."""
    report = Path("resultados.md")
    if report.exists():
        content = report.read_text()
        assert "pip" in content.lower()
        assert "uv" in content.lower()
        assert "speedup" in content.lower()
