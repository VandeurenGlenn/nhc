import setuptools

setuptools.setup(
    name='nhc',
    description='SDK for Niko Home Control',
    license='MIT',
    url='https://github.com/vandeurenglenn/nhc',
    version='0.3.2',
    author='vandeuren Glenn',
    author_email='vandeurenglenn@gmail.com',
    maintainer='vandeuren Glenn',
    maintainer_email='vandeurenglenn@gmail.com',
    long_description='Niko Home Control Client Library',
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['nclib'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
)
