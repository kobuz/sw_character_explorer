from django.core.files.base import ContentFile
from django.db import models

from characters import data_operations


class CollectionManager(models.Manager):
    def fetch_and_create(self):
        csv = data_operations.fetch_data_into_csv()
        collection = Collection.objects.create()
        collection.target_file.save(f"{collection.id}.csv", ContentFile(csv))
        return collection


class Collection(models.Model):
    target_file = models.FileField(upload_to="characters/")
    created = models.DateTimeField(auto_now_add=True)

    objects = CollectionManager()

    def __str__(self):
        return self.created.strftime("%Y-%m-%d %H:%M")
