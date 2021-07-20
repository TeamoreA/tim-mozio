from django.db import models

CURRENCY = (
    ('USD', 'US dollars'),
    ('EURO', 'Euros'),
    ('POUND', 'Pounds'),
    ('KSH', 'Kenyan Shillings'),
)


class Provider(models.Model):
    """
    Creates a model to hold a provider object instance
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    currency = models.CharField(max_length=100, choices=CURRENCY, default='USD')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Return a string representation of Provider object
        """
        return self.name
