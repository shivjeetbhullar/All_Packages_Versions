import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nse", 
    version="0.1.3",
    author="Shivjeet Singh Bhullar",
    author_email="bhullarshivjeet@gmail.com",
    description="Get Live Data From Nse And Filter It According To Your Choice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivjeetbhullar/nse",
    packages=setuptools.find_packages(),
    install_requires=["pi7db",'beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Database"
    ],
    python_requires='>=3.6',
)
