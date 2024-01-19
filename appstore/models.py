from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Application(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    title = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.URLField()  # url of the icon (assuming we store icons in S3)
    price = models.FloatField()
    link = models.URLField()
    is_verified = models.BooleanField(default=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.title)


class PurchasedApplication(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
