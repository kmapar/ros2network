from setuptools import setup

package_name = 'network'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kmapar',
    maintainer_email='kmapar@ucsd.edu',
    description='Package for networking functionality between service clients and server',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service_server = network.service_server_node:main',
        ],
    },
)
