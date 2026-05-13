from setuptools import setup

setup(
    name="bugbounty-cli",
    version="0.2.0",
    py_modules=[
        "main",
        "runner",
        "recon",
        "http_capture",
        "ai_agent",
        "enrichment",
        "reporting",
        "scope",
        "models",
        "screenshots",
    ],
    install_requires=["openai>=1.40.0", "requests>=2.31.0"],
    entry_points={"console_scripts": ["bugbounty=main:main"]},
    author="brownboi-tech",
    description="An AI-driven, modular CLI tool for automated bug bounty hunting.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brownboi-tech/Bug-Bounty-Cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
