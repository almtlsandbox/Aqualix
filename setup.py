#!/usr/bin/env python3
"""
Setup script for Aqualix - Underwater Image Processing Application
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join("docs", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Aqualix - Underwater Image Processing Application"

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="aqualix",
    version="1.0.0",
    author="Arnaud Dominique Lina",
    author_email="arnauddominique.lina@gmail.com",
    description="A comprehensive underwater image processing application with advanced algorithms",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/almtlsandbox/Aqualix",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "aqualix=main:main",
            "aqualix-cli=scripts.cli:main",
        ],
    },
    package_data={
        "config": ["*.json"],
        "tests": ["fixtures/*.jpg", "fixtures/*.png"],
    },
    include_package_data=True,
    zip_safe=False,
)
