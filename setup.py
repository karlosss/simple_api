import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-api",
    version="0.0.0.0.5",
    author="Karel Jilek",
    author_email="los.karlosss@gmail.com",
    description="A library to build a backend API (GraphQL) from Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karlosss/simple_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django==3.0.7",
        "graphene==2.1.8",
        "graphene-django==2.10.1",
    ],
    python_requires='>=3.6',
)
