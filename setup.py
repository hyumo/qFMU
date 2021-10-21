"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ 'wheel==0.33.6', 'jinja2', 'numpy' ]

test_requirements = ['pytest>=3', 'wheel==0.33.6', 'jinja2', 'numpy']

setup(
    author="Hang Yu",
    author_email='yuhang.neu@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="description",
    entry_points={
        'console_scripts': [
            'qfmu=qfmu.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords='qfmu',
    name='qfmu',
    packages=find_packages(include=['qfmu', 'qfmu.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hyumo/qfmu',
    version='0.1.0',
    zip_safe=False,
)

