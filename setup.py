"""The setup script."""

from setuptools import find_packages, setup

install_requires = open("requirements.txt").read().strip().split("\n")
dev_requires = open("requirements_dev.txt").read().strip().split("\n")

setup(
    name="qfmu",
    description="Quickly generate an FMU from command line",
    author="Hang Yu",
    author_email="yuhang.neu@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={
        "console_scripts": [
            "qfmu=qfmu.__main__:app",
        ],
    },
    license="BSD license",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="qfmu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"qfmu": ["codegen/templates/*", "codegen/include/*"]},
    test_suite="tests",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    url="https://github.com/hyumo/qfmu",
    version="0.2.4",
    zip_safe=False,
)
