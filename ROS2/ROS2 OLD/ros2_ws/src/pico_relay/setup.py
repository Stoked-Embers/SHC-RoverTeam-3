from setuptools import find_packages, setup

package_name = 'pico_relay'

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
    maintainer='tristan',
    maintainer_email='tristan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "relay = pico_relay.relay_node:main",
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.publisher_subscriber_function:main'
            'publisher = py_pubsub.publisher_member_function:main'
            'subscriber = py_pubsub.publisher_subscriber_function:main'
        ],
    },
)
