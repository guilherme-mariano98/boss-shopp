from setuptools import setup, find_packages

setup(
    name="boss-shopp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Django==4.2.7",
        "djangorestframework==3.14.0",
        "django-cors-headers==4.3.1",
        "python-decouple==3.8",
        "Pillow==10.0.1",
        "sqlparse==0.4.4"
    ],
    python_requires=">=3.8",
)