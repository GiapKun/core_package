from setuptools import setup, find_packages

# Đọc danh sách dependencies từ requirements.txt
def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line and not line.startswith("#")]

setup(
    name="core_package",
    version="0.1.0",
    author="GiapKun",
    author_email="trandinhgiap8051@gmail.com",
    description="A reusable core package for microservices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GiapKun/core_package",
    project_urls={
        "Bug Tracker": "https://github.com/GiapKun/core_package/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=parse_requirements("requirements.txt"),
)
