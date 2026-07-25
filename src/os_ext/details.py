import platform
import os

plat_str: str = f"{platform.machine()} {platform.system()} at {platform.node()} | {platform.platform()}"
posix_compatible = os.name == "posix"
