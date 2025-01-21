from setuptools import setup, find_packages

setup(
    name="hunterai_client",
    version="1.0.0",
    description="Python client library for interacting with HunterAI API",
    author="HuntersAI",
    url="https://github.com/your-repository/HunterAIClient",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
