from django.db import models


class Collection(models.Model):
    target_file = models.FileField(upload_to="characters/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.isoformat()
