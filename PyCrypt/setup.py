from setuptools import setup, find_packages

setup(
    name='pycryptsafe',
    version='1.0.0',
    description='Password-based file encryption CLI tool',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'cryptography>=41.0.0',
        'rich>=13.0.0',
        'typer[all]>=0.9.0',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'pycryptsafe=cli:app',
        ],
    },
    python_requires='>=3.9',
) 