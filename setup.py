from setuptools import setup, find_packages

setup(
    name="wapi",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.0.0",
        "PyQt6-WebEngine>=6.0.0"
    ],
    author="Egemen Geyik",
    author_email="muhammedegemengeyik@gmail.com",
    description="Cross-platform HTML/CSS/JS widget engine written in Python using PyQt6.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/egemngyk/wapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Widget Engines"
    ],
    python_requires=">=3.9",
)