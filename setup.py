from setuptools import setup, find_packages

setup(
    name="fundraising-analytics-dashboard",
    version="1.0.0",
    description="A comprehensive fundraising analytics dashboard with donor segmentation and ROI optimization",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Fundraising Analytics Team",
    author_email="analytics@example.com",
    url="https://github.com/your-username/fundraising-dashboard",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'plotly>=5.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Non-Profit Organizations",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="fundraising analytics donor segmentation roi optimization",
    project_urls={
        'Documentation': 'https://github.com/your-username/fundraising-dashboard/docs',
        'Source': 'https://github.com/your-username/fundraising-dashboard',
        'Tracker': 'https://github.com/your-username/fundraising-dashboard/issues',
    },
)