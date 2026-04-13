#!/usr/bin/env python3
"""
Script para generar la estructura del Módulo 16: Seguridad Moderna.
"""

from pathlib import Path

TEMAS_MODULO_16 = [
    "01_supply_chain_security",
    "02_dependency_attacks",
    "03_typosquatting_pypi",
    "04_malicious_packages",
    "05_sbom_introduccion",
    "06_sbom_formats_spdx_cyclonedx",
    "07_generacion_sboms_syft",
    "08_analisis_vulnerabilidades_sbom",
    "09_sbom_ci_cd",
    "10_sbom_signing",
    "11_sigstore_arquitectura",
    "12_keyless_signing_oidc",
    "13_firmar_wheels_cosign",
    "14_firmar_containers",
    "15_verificacion_firmas",
    "16_transparency_logs_rekor",
    "17_vulnerability_scanning_safety",
    "18_trivy_containers",
    "19_grype_scanning",
    "20_dependabot_github",
    "21_automatizacion_patching",
    "22_secrets_management_intro",
    "23_environment_variables",
    "24_secretos_ci_cd",
    "25_sops_introduccion",
    "26_sops_backends_age_kms",
    "27_sops_yaml_json",
    "28_sops_git_integration",
    "29_key_rotation_sops",
    "30_vault_arquitectura",
    "31_dynamic_secrets_vault",
    "32_vault_agents",
    "33_vault_python_hvac",
    "34_vault_kubernetes",
    "35_kubernetes_secrets",
    "36_external_secrets_operator",
    "37_sealed_secrets",
    "38_input_validation",
    "39_sql_injection_prevention",
    "40_xss_csrf_prevention",
]

def create_topic(base_path: Path, topic_name: str) -> None:
    """Crea estructura de un tema de seguridad."""
    topic_path = base_path / topic_name
    topic_path.mkdir(parents=True, exist_ok=True)
    
    for folder in ["examples", "exercises", "tests", "my_solution", "references"]:
        (topic_path / folder).mkdir(exist_ok=True)
    
    display_name = topic_name[3:].replace('_', ' ').title()
    
    readme = f"""# {display_name}

⏱️ **Tiempo estimado: 2-3 horas**

## 1. 📚 Definición

*[Por completar: 200-300 palabras sobre el concepto de seguridad]*

## 2. 💡 Aplicación Práctica

### Casos de Uso
1. 
2. 
3. 

### Código Ejemplo

```python
# Implementación segura
```

## 3. 🤔 ¿Por Qué Es Importante?

### Riesgos
- 
- 

### Impacto de No Implementar
- 
- 

## 4. 🔗 Referencias

- [OWASP](https://owasp.org/)
- [NIST Cybersecurity](https://www.nist.gov/cyberframework)
- *[Más referencias específicas]*

## 5. ✏️ Tarea de Práctica

### Nivel Básico
Identifica vulnerabilidades en código de ejemplo.

### Nivel Intermedio
Implementa mitigaciones y validaciones.

### Nivel Avanzado
Crea sistema completo con auditoría de seguridad.

## 6. 📝 Summary

- Punto clave 1
- Punto clave 2
- Mejores prácticas
- Herramientas recomendadas

## 7. 🧠 Mi Análisis Personal

> ✍️ Reflexiona sobre:
> - ¿Qué tan crítico es esto para tu proyecto?
> - ¿Qué vulnerabilidades has visto en producción?
> - ¿Cómo implementarías esto en tu stack?
"""
    
    (topic_path / "README.md").write_text(readme)
    
    links = f"""# Referencias: {display_name}

## Estándares y Frameworks
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Herramientas
- [Sigstore](https://www.sigstore.dev/)
- [SOPS](https://github.com/mozilla/sops)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Syft](https://github.com/anchore/syft)
- [Grype](https://github.com/anchore/grype)

## Documentación
- *[Añadir docs específicas del tema]*

## Artículos y Blogs
- *[Añadir artículos relevantes]*
"""
    
    (topic_path / "references" / "links.md").write_text(links)

def main():
    """Genera módulo 16."""
    base_path = Path(__file__).parent.parent / "16_security_moderna"
    base_path.mkdir(parents=True, exist_ok=True)
    
    print("🔒 Generando Módulo 16: Seguridad Moderna...")
    print()
    
    readme_module = """# Módulo 16: Seguridad Moderna 🔒

> Supply Chain, SBOM, Sigstore, SOPS, Vault, Container Security

## 📋 Descripción

Este módulo cubre las prácticas de seguridad más modernas para Python en 2026:
- Supply chain security
- Software Bill of Materials (SBOM)
- Keyless signing con Sigstore
- Gestión de secretos (SOPS, Vault)
- Container security
- Secure coding practices

## 🎯 Objetivos

- Proteger la supply chain de dependencias
- Generar y analizar SBOMs
- Firmar artefactos sin claves persistentes
- Gestionar secretos de forma segura
- Implementar security en CI/CD

## 📚 Contenido (40 Temas)

### Grupo 1: Supply Chain Security (4 temas)
Ataques, detección, prevención.

### Grupo 2: SBOM (6 temas)
Generación, análisis, integración en CI/CD.

### Grupo 3: Sigstore (6 temas)
Firma keyless, verificación, transparency logs.

### Grupo 4: Vulnerability Scanning (5 temas)
Herramientas modernas de análisis.

### Grupo 5: Secrets Management (13 temas)
SOPS, Vault, Kubernetes secrets.

### Grupo 6: Secure Coding (6 temas)
Prevención de vulnerabilidades comunes.

## ⏱️ Tiempo Total

**50-60 horas**

## 🔗 Referencias Principales

- [OWASP](https://owasp.org/)
- [Sigstore](https://www.sigstore.dev/)
- [SOPS](https://github.com/mozilla/sops)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
"""
    
    (base_path / "README.md").write_text(readme_module)
    
    # Crear todos los temas
    for i, topic in enumerate(TEMAS_MODULO_16, 1):
        create_topic(base_path, topic)
        if i % 10 == 0:
            print(f"  ✓ {i} temas creados...")
    
    print()
    print(f"✅ Módulo 16 generado: {len(TEMAS_MODULO_16)} temas")

if __name__ == "__main__":
    main()
