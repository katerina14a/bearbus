from django.db import models

class Route(models.Model):
    route_id = models.CharField(max_length=200)

    def __unicode__(self):
        return self.route_id

    def get_absolute_url(self):
        return "/routes/%i/" % self.id


class Stops(models.Model):
    intersection = models.CharField(max_length=200)

    def __unicode__(self):
        return self.intersection

    def get_absolute_url(self):
        return "/routes/%i/" % self.id