#!/usr/bin/env python3
"""
Script para completar los placeholders restantes en archivos de referencias.
"""

from pathlib import Path


def get_specific_content(topic_name: str) -> tuple[str, str]:
    """Retorna (documentación, artículos) específicos para cada tema de security."""

    topic_lower = topic_name.lower()

    # Supply Chain Security
    if "supply_chain" in topic_lower or "dependency_attack" in topic_lower:
        docs = """- [SLSA Framework](https://slsa.dev/)
- [Supply-chain Levels for Software Artifacts](https://slsa.dev/spec/v1.0/)
- [NIST SP 800-161](https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final)
- [CNCF Supply Chain Security](https://github.com/cncf/tag-security/tree/main/supply-chain-security)"""
        articles = """- [The State of Software Supply Chain Security (Sonatype)](https://www.sonatype.com/state-of-the-software-supply-chain)
- [Securing the Software Supply Chain (CNCF)](https://www.cncf.io/blog/2021/12/08/securing-the-software-supply-chain/)
- [Google: Know, Prevent, Fix Framework](https://security.googleblog.com/2023/08/toward-more-secure-software-supply-chain.html)
- [Supply Chain Attacks Explained](https://www.crowdstrike.com/cybersecurity-101/cyberattacks/supply-chain-attacks/)"""

    # SBOM
    elif "sbom" in topic_lower:
        docs = """- [SBOM Overview (CISA)](https://www.cisa.gov/sbom)
- [NTIA SBOM Documentation](https://www.ntia.gov/page/software-bill-materials)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [SPDX Specification](https://spdx.dev/specifications/)
- [Syft Documentation](https://github.com/anchore/syft#readme)"""
        articles = """- [A Practical Guide to SBOMs](https://www.linuxfoundation.org/blog/blog/a-summary-of-census-ii-open-source-software-application-libraries-the-world-depends-on)
- [SBOM at Scale (Chainguard)](https://chainguard.dev/unchained/sbom-at-scale)
- [Why SBOMs Are Critical](https://security.googleblog.com/2023/05/open-sourcing-our-progress-on-vsa.html)
- [SBOM Formats Comparison](https://www.aquasec.com/cloud-native-academy/supply-chain-security/sbom/)"""

    # Sigstore / Signing
    elif (
        "sigstore" in topic_lower
        or "signing" in topic_lower
        or "firmar" in topic_lower
        or "cosign" in topic_lower
        or "rekor" in topic_lower
        or "verificacion" in topic_lower
    ):
        docs = """- [Sigstore Documentation](https://docs.sigstore.dev/)
- [Cosign Documentation](https://docs.sigstore.dev/cosign/overview/)
- [Rekor Transparency Log](https://docs.sigstore.dev/rekor/overview/)
- [Fulcio Certificate Authority](https://docs.sigstore.dev/fulcio/overview/)
- [Cosign GitHub](https://github.com/sigstore/cosign)"""
        articles = """- [Introducing Sigstore](https://www.linuxfoundation.org/press/press-release/linux-foundation-announces-free-sigstore-signing-service)
- [Sigstore: A Solution for Software Supply Chain Security](https://www.chainguard.dev/unchained/sigstore-a-solution-to-software-supply-chain-security)
- [How Sigstore Works](https://blog.sigstore.dev/sigstore-build-verification/)
- [Keyless Signing with Sigstore](https://blog.sigstore.dev/cosign-2-0-released/)"""

    # SOPS
    elif "sops" in topic_lower:
        docs = """- [SOPS Documentation](https://github.com/mozilla/sops#readme)
- [SOPS with Age](https://github.com/mozilla/sops#22encrypting-using-age)
- [SOPS with KMS](https://github.com/mozilla/sops#23encrypting-using-aws-kms)
- [Age Encryption Tool](https://github.com/FiloSottile/age)"""
        articles = """- [Managing Secrets with SOPS](https://www.civo.com/learn/manage-secrets-in-your-kubernetes-cluster-using-sealed-secrets)
- [SOPS Best Practices](https://blog.gitguardian.com/secrets-management-tools/)
- [SOPS vs Sealed Secrets vs Vault](https://blog.container-solutions.com/kubernetes-secrets-management)
- [SOPS Tutorial](https://dev.to/stack-labs/manage-your-secrets-in-git-with-sops-common-operations-118g)"""

    # Vault
    elif "vault" in topic_lower or "hvac" in topic_lower or "dynamic_secret" in topic_lower:
        docs = """- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault Tutorials](https://developer.hashicorp.com/vault/tutorials)
- [Vault API](https://developer.hashicorp.com/vault/api-docs)
- [HVAC Python Client](https://hvac.readthedocs.io/)
- [Vault Architecture](https://developer.hashicorp.com/vault/docs/internals/architecture)"""
        articles = """- [Vault Getting Started](https://www.vaultproject.io/docs/what-is-vault)
- [Vault Best Practices](https://developer.hashicorp.com/vault/tutorials/recommended-patterns)
- [Dynamic Secrets in Vault](https://www.hashicorp.com/blog/why-we-need-dynamic-secrets)
- [Vault on Kubernetes](https://www.hashicorp.com/blog/injecting-vault-secrets-into-kubernetes-pods-via-a-sidecar)"""

    # Vulnerability Scanning
    elif (
        "vulnerability" in topic_lower
        or "scanning" in topic_lower
        or "trivy" in topic_lower
        or "grype" in topic_lower
        or "safety" in topic_lower
    ):
        docs = """- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Grype Documentation](https://github.com/anchore/grype#readme)
- [Safety Documentation](https://pyup.io/safety/)
- [Snyk for Python](https://docs.snyk.io/getting-started/supported-languages-and-frameworks/python)
- [CVE Database](https://www.cve.org/)"""
        articles = """- [Container Security Scanning Best Practices](https://sysdig.com/blog/dockerfile-best-practices/)
- [Vulnerability Management Best Practices](https://snyk.io/learn/vulnerability-management/)
- [CVE Database Overview](https://www.cve.org/About/Overview)
- [Scanning Python Dependencies](https://realpython.com/python-security-scanner/)"""

    # Kubernetes Secrets
    elif (
        "kubernetes" in topic_lower
        or "k8s" in topic_lower
        or "sealed" in topic_lower
        or "external_secret" in topic_lower
    ):
        docs = """- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [External Secrets Operator](https://external-secrets.io/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [Vault on Kubernetes](https://developer.hashicorp.com/vault/tutorials/kubernetes)
- [K8s Security Best Practices](https://kubernetes.io/docs/concepts/security/)"""
        articles = """- [Kubernetes Secrets Management](https://kubernetes.io/docs/concepts/security/)
- [Secret Management in Kubernetes](https://www.weave.works/blog/managing-secrets-in-kubernetes)
- [K8s Security Best Practices](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [External Secrets Operator Tutorial](https://www.cncf.io/blog/2022/03/08/kubernetes-external-secrets-operator/)"""

    # Typosquatting / Malicious Packages
    elif "typosquatting" in topic_lower or "malicious" in topic_lower:
        docs = """- [PyPI Security](https://pypi.org/security/)
- [Python Packaging Security](https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)"""
        articles = """- [Typosquatting Attacks on PyPI](https://www.reversinglabs.com/blog/python-packages-a-treasure-trove-of-malicious-code)
- [Malicious Packages in Open Source](https://blog.sonatype.com/pypi-and-npm-flooded-with-over-5000-dependency-confusion-copycats)
- [Protecting Against Typosquatting](https://blog.gitguardian.com/pypi-malicious-packages/)
- [Supply Chain Attacks via Dependencies](https://www.ndss-symposium.org/ndss-paper/towards-measuring-supply-chain-attacks-on-package-managers-for-interpreted-languages/)"""

    # Secrets Management / Environment Variables
    elif "secret" in topic_lower or "environment" in topic_lower or "ci_cd" in topic_lower:
        docs = """- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)"""
        articles = """- [Secrets Management Best Practices](https://blog.gitguardian.com/secrets-management-best-practices/)
- [Don't Commit Your Secrets](https://blog.gitguardian.com/secrets-credentials-api-git/)
- [Environment Variables Security](https://www.doppler.com/blog/environment-variables-security-best-practices)
- [CI/CD Security Best Practices](https://snyk.io/learn/secure-cicd-pipeline/)"""

    # Patching / Dependabot
    elif "patching" in topic_lower or "dependabot" in topic_lower:
        docs = """- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Renovate Bot](https://docs.renovatebot.com/)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)"""
        articles = """- [Automated Dependency Updates](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/)
- [Dependabot Best Practices](https://docs.github.com/en/code-security/dependabot/working-with-dependabot)
- [Vulnerability Patching Strategy](https://snyk.io/blog/best-practices-for-dependency-management/)"""

    # Input Validation / SQL Injection / XSS
    elif (
        "input" in topic_lower
        or "sql" in topic_lower
        or "xss" in topic_lower
        or "csrf" in topic_lower
        or "injection" in topic_lower
    ):
        docs = """- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)"""
        articles = """- [Preventing SQL Injection in Python](https://realpython.com/prevent-python-sql-injection/)
- [Web Security Best Practices](https://developer.mozilla.org/en-US/docs/Web/Security)
- [XSS Attack Examples](https://owasp.org/www-community/attacks/xss/)
- [CSRF Tokens Explained](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)"""

    else:
        # Genérico para otros temas de security
        docs = """- [Python Security Documentation](https://docs.python.org/3/library/security_warnings.html)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [CWE Top 25](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- [NIST Security Guidelines](https://csrc.nist.gov/publications)"""
        articles = """- [Secure Python Development](https://realpython.com/tutorials/security/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
- [Writing Secure Python Code](https://www.oreilly.com/library/view/secure-coding-in/9781449316686/)
- [Security in DevOps](https://www.redhat.com/en/topics/devops/what-is-devsecops)"""

    return docs, articles


def fix_placeholder_file(filepath: Path) -> bool:
    """Reemplaza placeholders en un archivo específico."""
    content = filepath.read_text()

    if "*[Añadir" not in content:
        return False

    # Extraer nombre del tema del path
    parts = filepath.parts
    topic_name = parts[-3]  # Dos niveles arriba de references/links.md

    # Obtener contenido específico
    docs, articles = get_specific_content(topic_name)

    # Reemplazar placeholders
    content = content.replace(
        "## Documentación\n- *[Añadir docs específicas del tema]*", f"## Documentación\n{docs}"
    )
    content = content.replace(
        "## Artículos y Blogs\n- *[Añadir artículos relevantes]*",
        f"## Artículos y Blogs\n{articles}",
    )

    # Añadir sección de comunidad si no existe
    if "## Comunidad" not in content and "16_security_moderna" in str(filepath):
        content += """\n## Comunidad y Recursos
- [r/netsec](https://www.reddit.com/r/netsec/)
- [OWASP Slack](https://owasp.org/slack/invite)
- [Cloud Native Security Day](https://events.linuxfoundation.org/cloud-native-securitycon/)
- [Security.txt](https://securitytxt.org/)
"""

    filepath.write_text(content)
    return True


def main():
    base = Path()
    fixed = 0

    # Buscar todos los archivos con placeholders
    for links_file in base.rglob("references/links.md"):
        if fix_placeholder_file(links_file):
            fixed += 1
            print(f"✓ {links_file.relative_to(base)}")

    print(f"\n✅ {fixed} archivos actualizados")


if __name__ == "__main__":
    main()
