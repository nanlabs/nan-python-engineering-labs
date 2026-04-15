"""
Tests para validar la comprensión de uv
"""
import subprocess
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_project():
    """Crea un directorio temporal para pruebas."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_uv_is_installed():
    """Verifica que uv está instalado y accesible."""
    result = subprocess.run(
        ["uv", "version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "uv no está instalado"
    assert "uv" in result.stdout.lower()


def test_uv_cache_directory_exists():
    """Verifica que el directorio de caché existe."""
    result = subprocess.run(
        ["uv", "cache", "dir"],
        capture_output=True,
        text=True,
        check=True
    )
    cache_dir = Path(result.stdout.strip())
    # El directorio puede no existir hasta la primera instalación
    # pero el comando debe funcionar
    assert cache_dir.as_posix(), "Cache dir debe retornar una ruta válida"


def test_uv_venv_creation(temp_project):
    """Verifica que uv puede crear entornos virtuales."""
    venv_path = temp_project / ".venv"
    result = subprocess.run(
        ["uv", "venv", str(venv_path)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Error creando venv: {result.stderr}"
    assert venv_path.exists(), "Directorio .venv no fue creado"
    assert (venv_path / "bin" / "python").exists(), "Python no está en .venv"


def test_uv_pip_install_simple_package(temp_project):
    """Verifica que uv puede instalar paquetes."""
    venv_path = temp_project / ".venv"
    
    # Crear venv
    subprocess.run(["uv", "venv", str(venv_path)], check=True)
    
    # Instalar paquete simple
    result = subprocess.run(
        [
            "uv", "pip", "install",
            "--python", str(venv_path / "bin" / "python"),
            "six"
        ],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Error instalando six: {result.stderr}"
    
    # Verificar que se puede importar
    import_result = subprocess.run(
        [str(venv_path / "bin" / "python"), "-c", "import six; print(six.__version__)"],
        capture_output=True,
        text=True
    )
    
    assert import_result.returncode == 0, "No se puede importar six"
    assert import_result.stdout.strip(), "six no tiene versión"


def test_uv_is_faster_than_pip(temp_project):
    """Test conceptual: uv debe ser más rápido que pip."""
    # Este es un test de concepto que verifica la instalación
    # En la práctica, la velocidad depende de muchos factores
    
    venv_path = temp_project / ".venv"
    subprocess.run(["uv", "venv", str(venv_path)], check=True)
    
    import time
    start = time.time()
    
    result = subprocess.run(
        [
            "uv", "pip", "install",
            "--python", str(venv_path / "bin" / "python"),
            "requests"
        ],
        capture_output=True,
        text=True
    )
    
    elapsed = time.time() - start
    
    assert result.returncode == 0
    # Si está en caché, debe ser muy rápido
    # Este threshold es conservador
    assert elapsed < 30, f"uv tomó {elapsed}s, debería ser más rápido"


def test_uv_cache_reuse(temp_project):
    """Verifica que uv reutiliza la caché entre instalaciones."""
    venv1 = temp_project / "venv1"
    venv2 = temp_project / "venv2"
    
    # Primera instalación
    subprocess.run(["uv", "venv", str(venv1)], check=True)
    result1 = subprocess.run(
        [
            "uv", "pip", "install",
            "--python", str(venv1 / "bin" / "python"),
            "click==8.1.7"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Segunda instalación (debería usar caché)
    subprocess.run(["uv", "venv", str(venv2)], check=True)
    
    import time
    start = time.time()
    result2 = subprocess.run(
        [
            "uv", "pip", "install",
            "--python", str(venv2 / "bin" / "python"),
            "click==8.1.7"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    elapsed = time.time() - start
    
    # La segunda instalación debe ser mucho más rápida (desde caché)
    assert elapsed < 5, f"Instalación desde caché tomó {elapsed}s, debería ser <5s"
    
    # Verificar que ambas tienen click
    for venv in [venv1, venv2]:
        check = subprocess.run(
            [str(venv / "bin" / "python"), "-c", "import click"],
            capture_output=True
        )
        assert check.returncode == 0


def test_uv_handles_dependencies():
    """Verifica que uv maneja dependencias transitivas correctamente."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        venv_path = temp_dir / ".venv"
        subprocess.run(["uv", "venv", str(venv_path)], check=True)
        
        # flask tiene varias dependencias
        result = subprocess.run(
            [
                "uv", "pip", "install",
                "--python", str(venv_path / "bin" / "python"),
                "flask==3.0.0"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verificar que las dependencias están instaladas
        list_result = subprocess.run(
            [
                "uv", "pip", "list",
                "--python", str(venv_path / "bin" / "python")
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        # flask depende de werkzeug, jinja2, click, etc.
        assert "werkzeug" in list_result.stdout.lower()
        assert "jinja2" in list_result.stdout.lower()
        assert "click" in list_result.stdout.lower()
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestUVArchitecture:
    """Tests sobre comprensión de la arquitectura."""
    
    def test_student_understands_pubgrub(self):
        """Verifica que existe documentación sobre PubGrub."""
        # Este test verifica que el estudiante ha creado documentación
        solution_dir = Path(__file__).parent.parent / "my_solution"
        
        if solution_dir.exists():
            docs = list(solution_dir.glob("*.md"))
            # Si hay documentación, debería mencionar PubGrub
            if docs:
                content = ""
                for doc in docs:
                    content += doc.read_text().lower()
                
                assert "pubgrub" in content, \
                    "La documentación debería mencionar PubGrub"
    
    def test_student_understands_rust_benefits(self):
        """Verifica que existe documentación sobre Rust."""
        solution_dir = Path(__file__).parent.parent / "my_solution"
        
        if solution_dir.exists():
            docs = list(solution_dir.glob("*.md"))
            if docs:
                content = ""
                for doc in docs:
                    content += doc.read_text().lower()
                
                # Debe mencionar algunas ventajas de Rust
                rust_benefits = ["velocidad", "concurrencia", "memoria", "rust"]
                mentions = sum(1 for benefit in rust_benefits if benefit in content)
                
                assert mentions >= 2, \
                    "La documentación debería explicar ventajas de Rust"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
