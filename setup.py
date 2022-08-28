import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pympt",
    description="A simlpe Merkle Patricia Trie implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nynra/pympt",
    packages=setuptools.find_packages(),
    install_requires=[
        'cytoolz==0.9.0.1',
        'eth-hash==0.2.0',
        'eth-typing==2.0.0',
        'eth-utils==1.4.1',
        'pycryptodome==3.7.3',
        'rlp==1.1.0',
        'toolz==0.9.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography"
    ],
)
