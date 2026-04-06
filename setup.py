"""
Setup configuration for simulation project.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="EDT_simulation_project",
    version="0.1.0",
    author="Nsy Richie",
    author_email="tanrichie99@gmail.com",
    description="Simulation framework with Blender-PyTorch integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "pyyaml>=6.0",
        "trimesh>=3.23.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "sim-run=main:main",
        ],
    },
)