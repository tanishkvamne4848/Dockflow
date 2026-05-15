from setuptools import setup, find_packages

setup(
    name="dockflow",
    version="1.0.0",
    description="Automated molecular docking pipeline (Vina + RDKit + PDBFixer)",
    author="dockflow",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "pandas",
        "pyyaml",
        "tqdm",
        "rich",
        "fastapi",
        "uvicorn",
        "openmm",
        "pdbfixer",
        # RDKit is best installed via conda-forge; pip wheel may work on some systems.
        "rdkit",
    ],
    entry_points={
        "console_scripts": [
            "dockflow=cli:main"
        ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
