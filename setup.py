from setuptools import setup, find_packages

setup(
    name="pyslide",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # 我们不需要额外的依赖项
    python_requires=">=3.7",
    author="Jingwen Gu",
    author_email="jingwengu0829@gmail.com",
    description="Interactive Python Code Presentations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JingwenGu0829/PySlide",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 