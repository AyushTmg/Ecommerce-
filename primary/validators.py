from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_file_size=100
    if file.size>max_file_size*1024:
        raise ValidationError(f"File is too Large\n The file can't be larger than {max_file_size} KB")
    