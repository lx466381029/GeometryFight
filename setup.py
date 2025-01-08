from setuptools import setup, find_packages
import os

# 如果README.md文件不存在，使用空字符串作为描述
if os.path.exists("README.md"):
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()
    except UnicodeDecodeError:
        long_description = "A geometric shooting game"
else:
    long_description = "A geometric shooting game"

setup(
    name="geometry-fight",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A geometric shooting game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geometry-fight",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.5.2",
    ],
) 