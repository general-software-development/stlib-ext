# os_ext.details

## Contents

`plat_str: str`
: A pre-computed human-readable string that represents the OS, the OS version, CPU architecture, etc.
: Example 1: `x86_64 Linux at DESKTOP-ABCDEFG | Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.42`
: Example 2: `AMD64 Windows at DESKTOP-ABCDEFG | Windows-11-10.0.26100-SP0`

`posix_compatible: bool`
: Whether the operating system is POSIX-compatible (`True`) or non-POSIX (`False`).
