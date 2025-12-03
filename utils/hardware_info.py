"""
Hardware information collection for benchmark metadata.
"""
import platform
import os


def get_hardware_info() -> dict:
    """
    Collect hardware and system information.

    Returns:
        Dictionary containing system and hardware details.
    """
    info = {}

    # Operating System
    info['os'] = platform.system()
    info['os_version'] = platform.version()
    info['os_release'] = platform.release()

    # Python Version
    info['python_version'] = platform.python_version()

    # Processor
    info['processor'] = platform.processor()
    info['machine'] = platform.machine()

    # CPU Count
    info['cpu_count'] = os.cpu_count()

    # Platform
    info['platform'] = platform.platform()

    return info


def format_hardware_info(info: dict = None) -> str:
    """
    Format hardware information for markdown display.

    Args:
        info: Hardware info dictionary. If None, will collect it.

    Returns:
        Formatted string for markdown display.
    """
    if info is None:
        info = get_hardware_info()

    lines = []
    lines.append("## 💻 System Information")
    lines.append("")
    lines.append(f"- **OS**: {info['os']} {info['os_release']}")
    lines.append(f"- **Python**: {info['python_version']}")
    lines.append(f"- **Processor**: {info['processor']}")
    lines.append(f"- **CPU Cores**: {info['cpu_count']}")
    lines.append("")

    return "\n".join(lines)


def format_hardware_info_compact(info: dict = None) -> str:
    """
    Format hardware information in a compact single-line format.

    Args:
        info: Hardware info dictionary. If None, will collect it.

    Returns:
        Compact formatted string.
    """
    if info is None:
        info = get_hardware_info()

    return f"{info['os']} {info['os_release']} | Python {info['python_version']} | {info['processor']} ({info['cpu_count']} cores)"

