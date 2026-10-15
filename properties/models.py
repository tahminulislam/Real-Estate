
from datetime import timedelta

from django.db import models
from django.utils import timezone


class Property(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="properties/")
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FeaturedOffer(models.Model):
    DURATION_CHOICES = [
        (24, "24 Hours"),
        (48, "2 Days"),
        (168, "7 Days"),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="offers/")
    description = models.TextField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=200, blank=True)

    duration_hours = models.PositiveIntegerField(
        choices=DURATION_CHOICES,
        default=24,
    )

    starts_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(editable=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.expires_at = self.starts_at + timedelta(
            hours=self.duration_hours
        )
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_currently_active(self):
        now = timezone.now()
        return (
            self.is_active
            and self.starts_at <= now < self.expires_at
        )

    class Meta:
        ordering = ["-starts_at"]

    def __str__(self):
        return self.title
