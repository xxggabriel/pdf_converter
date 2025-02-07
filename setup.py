from setuptools import setup, find_packages

setup(
    name='pdf_converter',
    version='0.1.0',    
    description='A simple example package',
    url='https://github.com/xxggabriel/pdf_converter',
    author='Gabriel Oliveira',
    author_email='gabrielsouza2@discente.ufg.br',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF==1.25.3',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)