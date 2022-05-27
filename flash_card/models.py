from django.db import models


class Deck(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

    def get_image_folder(self):
        return str(self.image)[6:]

    class Meta:
        ordering = ['updated_at']


class Card(models.Model):
    title = models.CharField(max_length=200)
    answer = models.CharField(max_length=300)
    icon = models.ImageField(upload_to='static/photos/icons/%Y/%m/%d', null=True, blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    view = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.__str__()

    def get_icon_forder(self):
        return str(self.image)[6:]

    class Meta:
        ordering = ['-updated_at']