from setuptools import find_packages, setup

setup(
    name="bugbounty-cli",
    version="0.2.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["openai>=1.40.0", "requests>=2.31.0"],
    entry_points={
        "console_scripts": [
            "hexa-ai=hexa_ai.main:main",
            "hexa-ai-server=hexa_ai.api_server:main",
        ]
    },
)
