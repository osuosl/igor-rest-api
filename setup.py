from setuptools import setup, find_packages

setup(
    name="igor-rest-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask==0.10.1",
        "Flask-HTTPAuth==2.2.1",
        "Flask-RESTful==0.3.0",
        "Flask-SQLAlchemy==1.0",
        "Flask-Script==2.0.5",
        "Flask-Testing==0.4.2",
        "Jinja2==2.7.3",
        "MarkupSafe==0.23",
        "SQLAlchemy==0.9.4",
        "Werkzeug==0.9.6",
        "aniso8601==0.82",
        "click==2.1",
        "itsdangerous==0.24",
        "nose==1.3.3",
        "pexpect==3.3",
        "pyipmi==0.11.0",
        "pytz==2014.3",
        "requests==2.3.0",
        "six==1.6.1",
    ],
    dependency_links=[
        "git+https://github.com/emaadmanzoor/pyipmi.git@17d41fa34abc1be487b6d68da9b33d205fd1529e#egg=pyipmi-0.11.0"
    ],
    entry_points={
        'console_scripts': [
            'igor-manage = igor_rest_api.management:run'
        ]
    },
    test_suite = 'nose.collector'
)
