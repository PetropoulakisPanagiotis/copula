from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "numpy>=1.16",
    "copulae>=0.5.2",
    "scipy>=1.4.1",
    "pandas>=1.0.3",
]

setup(
    name="copula",
    version="1.0.0",
    author="VeniArakelian",
    author_email="veniarakelian@yahoo.com",
    download_url="https://github.com/PetropoulakisPanagiotis/copula/archive/master.zip",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    keywords=["copula"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ]
)
