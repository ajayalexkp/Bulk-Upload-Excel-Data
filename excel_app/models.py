from django.db import models

# Create your models here.


class CustomerAddress(models.Model):
    address = models.TextField(max_length=120)

    def __str__(self):
        return self.address


class CustomerDetails(models.Model):
    name = models.CharField(max_length=60, null=True)
    gender = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
