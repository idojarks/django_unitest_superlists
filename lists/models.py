from django.db import models
from django.urls import reverse

class List(models.Model):
    
    def get_absolute_url(self):
        return reverse("view_list", kwargs={'id':self.id})
    

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        #unique_together = ('list', 'text')
        constraints = [
            models.UniqueConstraint(fields=['list', 'text'], name='unique list and text')
        ]
        ordering = ('id',)

    def __str__(self):
        return self.text
