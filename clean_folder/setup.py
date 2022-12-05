from setuptools import setup, find_namespace_packages

setup(
    name="clean-folder",
    version="0.1.3",
    description="The package sorts the files in the folder",
    url="https://github.com/ruslan-kornich/GoIT_task_7.git",
    author="Kornich Ruslan",
    author_email="ruslan.kornich@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["clean-folder = clean_folder.clean:main"]},
    package_dir={"clean_folder": "clean_folder"},
)
