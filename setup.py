from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="package_core",
    version="0.1.1",
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=requirements,
    author="Gavin Tran",
    author_email="trandinhgiap8051@gmail.com",
    description="My private package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Private :: Do Not Distribute",
        "Operating System :: OS Independent",
    ],
)
