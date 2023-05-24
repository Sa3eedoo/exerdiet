from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_mb = 50

    if image.size > max_size_mb * (2 ** 20):
        raise ValidationError(f'Images cannot be larger than {max_size_mb}MB!')
