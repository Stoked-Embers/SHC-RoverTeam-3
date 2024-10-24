from setuptools import find_packages, setup

package_name = 'data_relay'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wyatt',
    maintainer_email='wyattahoward@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "talker_node = data_relay.talker:main",
            "listener_node = data_relay.listener:main",
            "groundstation_node = data_relay.groundstation_node:main"
        ],
    },
)
