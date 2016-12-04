from setuptools import setup, find_packages


setup(
    name='teamplayer-rotation',
    version='0.0',
    description='Fill strategy to play songs in rotation',
    author='Albert Hopkins',
    author_email='marduk@python.net',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'teamplayer',
    ],
    include_package_data=True,
    entry_points={
        'teamplayer.autofill_strategy': [
            'rotation = teamplayer_rotation.autofill:rotation_autofill',
        ]
    },
)
