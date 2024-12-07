from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'kabot_launcher'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'description/urdf'), glob('description/urdf/*.xacro')),
        (os.path.join('share', package_name, 'description/meshes'), glob('description/models/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jk',
    maintainer_email='jakubkolasa99@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
