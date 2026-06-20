"""System readiness check — run before installing VoxCPM2."""

import sys
import importlib.util
import subprocess


def _check_python() -> tuple[bool, str]:
    major, minor = sys.version_info[:2]
    ok = (major == 3) and (10 <= minor <= 12)
    return ok, f"Python {major}.{minor} {'✓' if ok else '✗  (нужно 3.10–3.12)'}"


def _check_torch() -> tuple[bool, str]:
    spec = importlib.util.find_spec("torch")
    if spec is None:
        return False, "PyTorch не е инсталиран  ✗"
    import torch
    from packaging.version import Version
    ok = Version(torch.__version__.split("+")[0]) >= Version("2.5.0")
    return ok, f"PyTorch {torch.__version__} {'✓' if ok else '✗  (нужно ≥ 2.5.0)'}"


def _check_cuda() -> tuple[bool, str]:
    try:
        import torch
        if not torch.cuda.is_available():
            return False, "CUDA не е наличен  ✗"
        ver = torch.version.cuda or ""
        from packaging.version import Version
        ok = Version(ver) >= Version("12.0")
        return ok, f"CUDA {ver} {'✓' if ok else '✗  (нужно ≥ 12.0)'}"
    except Exception as e:
        return False, f"CUDA проверка неуспешна: {e}  ✗"


def _check_vram() -> tuple[bool, str]:
    try:
        import torch
        if not torch.cuda.is_available():
            return False, "GPU не е открит  ✗"
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        ok = vram_gb >= 8
        name = torch.cuda.get_device_name(0)
        return ok, f"{name} — {vram_gb:.1f} GB VRAM {'✓' if ok else '✗  (нужно ≥ 8 GB)'}"
    except Exception as e:
        return False, f"VRAM проверка неуспешна: {e}  ✗"


def run() -> bool:
    checks = [_check_python(), _check_torch(), _check_cuda(), _check_vram()]
    print("\n── VoxCPM2 Диагностика ──────────────────")
    all_ok = True
    for ok, msg in checks:
        print(f"  {msg}")
        if not ok:
            all_ok = False
    print("─────────────────────────────────────────")
    if all_ok:
        print("  ✓  Готов за VoxCPM2\n")
    else:
        print("  ✗  Реши проблемите по-горе преди инсталация\n")
    return all_ok


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
