from setuptools import setup, find_packages

setup(
    name='flask_app_3',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.0.3',
        'SQLAlchemy==1.4.31',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-Migrate==3.1.0',
        'Flask-Caching==2.0.2',
        'redis==5.0.1',
        'psycopg2-binary==2.9.3',
        'werkzeug==2.0.3',
        'gunicorn==20.1.0',
    ],
)