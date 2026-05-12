from setuptools import setup, find_packages

setup(
    name='bugbounty-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai',
        'requests',
        'google-generativeai',
    ],
    entry_points={
        'console_scripts': [
            'bugbounty=main:main',
        ],
    },
    author='brownboi-tech',
    description='An AI-driven, modular CLI tool for automated bug bounty hunting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/brownboi-tech/Bug-Bounty-Cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
