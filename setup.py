from setuptools import setup, find_packages

setup(
    name="analyze-cli",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi"
    ],
    entry_points={
        "console_scripts": [
            "analyze = analyze:main"
        ],
    },
)
