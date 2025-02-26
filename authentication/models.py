from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class UserRole(models.TextChoices):
    DRIVER = "driver", "Driver"
    CUSTOMER = "customer", "Customer"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True, default=None)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER
    )

    class Meta:
        db_table = "users"

    @classmethod
    def is_password_correct(cls, user_entered_password, actual_password):
        return user_entered_password == actual_password

    def save(self, *args, **kwargs):
        if self.password and (
            not self.pk
            or not User.objects.filter(pk=self.pk, password=self.password).exists()
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
