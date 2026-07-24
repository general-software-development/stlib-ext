#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=('tests', 'lint', 'clear-docker', 'clean', 'clean-ultra'))

args = parser.parse_args()

import subprocess
import os
from pathlib import Path
import shutil

def toInt(a: str) -> int:
    a = a.strip()
    if a.isnumeric():
        return int(a)
    return 0

if args.action == 'tests':
    subprocess.run(['docker', 'build', '-f', 'scripts/Dockerfile.base', '-t', 'stlib-ext-environment', '.'])
    subprocess.run(['docker', 'build', '-f', 'tests/Dockerfile', '-t', 'stlib-tests', '.'])
    subprocess.run(['docker', 'run', '-t', '--rm', 'stlib-tests'])
elif args.action == 'clear-docker':
    subprocess.run(['docker', 'rmi', 'stlib-tests'])
    subprocess.run(['docker', 'rmi', 'stlib-lint'])
    subprocess.run(['docker', 'rmi', 'stlib-ext-environment'])
    subprocess.run(['docker', 'image', 'prune', '-f'])
elif args.action == 'clean':
    origSize = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(".") for file in files)

    for directory in ("dist", ".mypy_cache", ".pytest_cache", "site"):
        path = Path(directory)
        if path.exists():
            print(f"CMD\t\tRM -R\t{path}")
            shutil.rmtree(path)

    for path in Path(".").rglob("__pycache__"):
        print(f"CMD\t\tRM -R\t{path}")
        shutil.rmtree(path)

    newSize = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(".") for file in files)

    print(f"DIFF\t\t-{round((origSize-newSize) / 1024)}KB")
elif args.action == 'clean-ultra':
    origSize = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(".") for file in files)

    for directory in ("dist", ".mypy_cache", ".pytest_cache", "site"):
        path = Path(directory)
        if path.exists():
            print(f"CMD\t\tRM -R\t{path}")
            shutil.rmtree(path)

    for path in Path(".").rglob("__pycache__"):
        print(f"CMD\t\tRM -R\t{path}")
        shutil.rmtree(path)

    print("CMD\t\tUV CACHE PRUNE")
    result = subprocess.run(['uv', 'cache', 'prune'], capture_output=True, text=True)
    out = result.stdout + result.stderr
    print("\t\t#  " + out.replace('\n', "\n\t\t#  "))

    newSize = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(".") for file in files)

    dockerOrigSize = toInt(subprocess.run(["docker", "image", "inspect", "stlib-tests", "--format='{{.Size}}'"], capture_output=True, text=True).stdout) \
                        + toInt(subprocess.run(["docker", "image", "inspect", "stlib-ext-environment", "--format='{{.Size}}'"], capture_output=True, text=True).stdout) \
                        + toInt(subprocess.run(["docker", "system", "df", "--format", ""'{{if eq .Type "Images"}}{{.Size}}{{end}}'""], capture_output=True, text=True).stdout)

    subprocess.run(['docker', 'rmi', 'stlib-tests'], capture_output=True, text=True)
    subprocess.run(['docker', 'rmi', 'stlib-lint'], capture_output=True, text=True)
    subprocess.run(['docker', 'rmi', 'stlib-ext-environment'], capture_output=True, text=True)
    subprocess.run(['docker', 'image', 'prune', '-f'], capture_output=True, text=True)
    print("CMD\t\tDOCKER RMI\t\tstlib-tests")
    print("CMD\t\tDOCKER RMI\t\tstlib-ext-environment")
    print("CMD\t\tDOCKER IMAGE PRUNE")

    dockerNewSize = toInt(subprocess.run(["docker", "image", "inspect", "stlib-tests", "--format='{{.Size}}'"], capture_output=True, text=True).stdout) \
                            + toInt(subprocess.run(["docker", "image", "inspect", "stlib-ext-environment", "--format='{{.Size}}'"], capture_output=True, text=True).stdout) \
                            + toInt(subprocess.run(["docker", "system", "df", "--format", ""'{{if eq .Type "Images"}}{{.Size}}{{end}}'""], capture_output=True, text=True).stdout)
    
    print(f"DIFF\t\t-{round((origSize-newSize+dockerOrigSize-dockerNewSize) / 1024)}KB")
elif args.action == 'lint':
    subprocess.run(['docker', 'build', '-f', 'scripts/Dockerfile.base', '-t', 'stlib-ext-environment', '.'])
    subprocess.run(['docker', 'build', '-f', 'scripts/Dockerfile.mypy', '-t', 'stlib-lint', '.'])
    subprocess.run(['docker', 'run', '-t', '--rm', 'stlib-lint'])
