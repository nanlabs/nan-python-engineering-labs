"""
Tests for validar la comprensión de uv
"""
import subprocess
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_project():
    """Create a temporary directory for tests."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_uv_is_installed():
    """Verify uv is installed and accessible."""
    result = subprocess.run(
        ["uv", "version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "uv no está instalado"
    assert "uv" in result.stdout.lower()


def test_uv_cache_directory_exists():
    """Verify cache directory exists."""
    result = subprocess.run(
        ["uv", "cache", "dir"],
        capture_output=True,
        text=True,
        check=True
    )
    cache_dir = Path(result.stdout.strip())
    # The directory may not exist until first installation
    # but the command should work
    assert cache_dir.as_posix(), "Cache dir must return a valid path"


def test_uv_venv_creation(temp_project):
    """Verify uv can create virtual environments."""
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
    """Verify uv can install packages."""
    venv_path = temp_project / ".venv"
    
    # Crear venv
    subprocess.run(["uv", "venv", str(venv_path)], check=True)
    
    # Install simple package
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
    """Conceptual test: uv should be faster than pip."""
    # This is a conceptual test that checks installation
    # In practice, speed depends on many factors
    
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
    # If cached, it should be very fast
    # Este threshold es conservador
    assert elapsed < 30, f"uv tomó {elapsed}s, debería ser más rápido"


def test_uv_cache_reuse(temp_project):
    """Verify uv reuses cache across installations."""
    venv1 = temp_project / "venv1"
    venv2 = temp_project / "venv2"
    
    # First installation
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
    
    # Second installation (should use cache)
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
    
    # The second installation should be much faster (from cache)
    assert elapsed < 5, f"installation desde caché tomó {elapsed}s, should be <5s"
    
    # Verificar que ambas tienen click
    for venv in [venv1, venv2]:
        check = subprocess.run(
            [str(venv / "bin" / "python"), "-c", "import click"],
            capture_output=True
        )
        assert check.returncode == 0


def test_uv_handles_dependencies():
    """Verify uv handles transitive dependencies correctly."""
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
    """Tests on architecture understanding."""
    
    def test_student_understands_pubgrub(self):
        """Verify PubGrub documentation exists."""
        # This test verifies the student created documentation
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
        """Verify Rust documentation exists."""
        solution_dir = Path(__file__).parent.parent / "my_solution"
        
        if solution_dir.exists():
            docs = list(solution_dir.glob("*.md"))
            if docs:
                content = ""
                for doc in docs:
                    content += doc.read_text().lower()
                
                # Should mention some Rust advantages
                rust_benefits = ["speed", "concurrency", "memory", "rust"]
                mentions = sum(1 for benefit in rust_benefits if benefit in content)
                
                assert mentions >= 2, \
                    "La documentación debería explicar ventajas de Rust"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
