import setuptools

setuptools.setup(
    name = "shoplist_app",
    version = "0.0.1",
    author = "A.Noordervliet",
    author_email = "amber.noordervliet@student.uva.nl",
    python_requires = ">=3.6",
    install_requires=[
        "bcrypt",  
        "Flask",       
        "Flask-SQLAlchemy", 
        "Flask-Login",
        "Flask-WTF",
        "SQLAlchemy",
        "WTForms"
    ],
    packages = setuptools.find_packages()
)
