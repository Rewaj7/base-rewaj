from setuptools import setup, find_packages
from pathlib import Path

requirements_path = Path(__file__).parent / "requirements.txt"
with requirements_path.open() as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="analyze-cli",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "analyze = analyze:main"
        ],
    },
)