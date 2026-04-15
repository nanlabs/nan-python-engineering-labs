"""
Ejemplo: Instalación y verificación de uv en diferentes entornos
"""
import subprocess
import platform
import sys
from pathlib import Path


def check_uv_installation():
    """Verifica si uv está instalado correctamente."""
    print("🔍 Verificando instalación de uv\n")
    
    try:
        # Versión
        result = subprocess.run(
            ["uv", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ uv instalado: {version}")
        
        # Ubicación
        result = subprocess.run(
            ["which", "uv"],
            capture_output=True,
            text=True,
            check=True
        )
        location = result.stdout.strip()
        print(f"📍 Ubicación: {location}")
        
        # Tamaño del binario
        size_mb = Path(location).stat().st_size / (1024 * 1024)
        print(f"💾 Tamaño: {size_mb:.2f} MB")
        
        return True
    
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv no está instalado")
        return False


def show_system_info():
    """Muestra información del sistema."""
    print(f"\n📊 Información del Sistema")
    print(f"{'='*50}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Arquitectura: {platform.machine()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"{'='*50}\n")


def show_configuration():
    """Muestra configuración actual de uv."""
    print("⚙️  Configuración de uv\n")
    
    # Cache directory
    try:
        result = subprocess.run(
            ["uv", "cache", "dir"],
            capture_output=True,
            text=True,
            check=True
        )
        cache_dir = Path(result.stdout.strip())
        print(f"📁 Cache directory: {cache_dir}")
        
        if cache_dir.exists():
            # Tamaño de caché
            result = subprocess.run(
                ["du", "-sh", str(cache_dir)],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                print(f"💾 Tamaño de caché: {size}")
        else:
            print("   (Caché aún no existe)")
    
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error obteniendo configuración: {e}")
    
    # Variables de entorno relevantes
    print(f"\n🔧 Variables de Entorno Relevantes:")
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
            print(f"   {var}=(no configurada)")


def show_available_commands():
    """Lista comandos disponibles en uv."""
    print(f"\n📚 Comandos Disponibles\n")
    
    result = subprocess.run(
        ["uv", "--help"],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Parsear comandos
    lines = result.stdout.split('\n')
    in_commands = False
    
    for line in lines:
        if 'Commands:' in line:
            in_commands = True
            continue
        
        if in_commands and line.strip():
            if line.startswith('  ') and not line.startswith('   '):
                # Es un comando
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    cmd, desc = parts
                    print(f"   • {cmd:12} {desc}")
            elif not line.startswith('  '):
                break


def demonstrate_config_file():
    """Demuestra la creación de un archivo de configuración."""
    print(f"\n📝 Ejemplo de Archivo de Configuración\n")
    
    config_content = """
# .uv/config.toml - Configuración local del proyecto

[tool.uv]
# Índice principal de paquetes
index-url = "https://pypi.org/simple"

# Índices adicionales (por ejemplo, índices privados)
# extra-index-url = ["https://private.pypi.org/simple"]

[tool.uv.pip]
# No usar binarios pre-compilados para estos paquetes
# no-binary = ["scipy"]

# Solo usar wheels (no compilar desde source)
# only-binary = [":all:"]

[tool.uv.resolution]
# No permitir pre-releases
prerelease = "disallow"

# Estrategia de resolución
# resolution = "highest"  # o "lowest" o "lowest-direct"
"""
    
    print(config_content)
    
    # Preguntar si crear el archivo
    response = input("¿Crear este archivo en el directorio actual? (s/n): ")
    if response.lower() == 's':
        config_path = Path.cwd() / ".uv" / "config.toml"
        config_path.parent.mkdir(exist_ok=True)
        config_path.write_text(config_content.strip())
        print(f"✅ Archivo creado en: {config_path}")


if __name__ == "__main__":
    print("🚀 uv: Instalación y Configuración\n")
    
    show_system_info()
    
    if not check_uv_installation():
        print("\n💡 Para instalar uv, ejecuta:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    show_configuration()
    show_available_commands()
    demonstrate_config_file()
    
    print(f"\n✨ ¡Configuración completa!")
