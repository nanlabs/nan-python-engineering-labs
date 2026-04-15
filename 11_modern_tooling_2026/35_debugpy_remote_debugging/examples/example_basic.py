"""debugpy: remote debugging attach demo."""


def attach_config(host: str = "localhost", port: int = 5678) -> dict[str, object]:
    return {
        "type": "python",
        "request": "attach",
        "connect": {"host": host, "port": port},
        "pathMappings": [{"/app": "${workspaceFolder}"}],
    }


def launch_snippet(port: int = 5678) -> list[str]:
    return [
        "import debugpy",
        f"debugpy.listen({port})",
        "debugpy.wait_for_client()  # blocks until debug client attaches",
        "# Your code continues here...",
    ]


def main() -> None:
    cfg = attach_config()
    print("VS Code launch.json snippet:")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
    print("\nScript header for remote debug:")
    for line in launch_snippet():
        print(f"  {line}")


if __name__ == "__main__":
    main()
