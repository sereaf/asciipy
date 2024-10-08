from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='asciipy',
	version='0.1.0',
	description='This package lets you turn images and videos to ascii art and print it to terminal or save it in a supported format on your computer.',
	author='Sereaf',
	author_email='asciipycontact@gmail.com',
	url='https://github.com/sereaf/asciipy',
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
        'opencv-python',
        'Pillow',
        'numpy'
    ],
    extras_require = {
        'audio': ['ffmpeg-python']
    },
	classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
	keywords='ascii video image opencv pillow terminal text',
	entry_points={
        "console_scripts": [
            'asciipy=asciipy.cli:main'
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)
