"""Main Module"""

from modules.transformation import AudioTransformer


# Create objects for classes
transformer = AudioTransformer()

print('##############################################')
print('\tTRANSFORM AUDIO FILES')
print('##############################################')
transformer.transform()
