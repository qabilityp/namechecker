from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    independent = models.BooleanField(default=True)
    google_maps = models.URLField(max_length=500, blank=True, null=True)
    open_street_maps = models.URLField(max_length=500, blank=True, null=True)
    capital = models.TextField(blank=True, null=True)
    capital_coordinates = models.TextField(blank=True, null=True)
    flags = models.URLField(max_length=500, blank=True, null=True)
    flags_svg = models.URLField(max_length=500, blank=True, null=True)
    flaf_alt = models.TextField(blank=True, null=True)
    coat_of_arms_png = models.URLField(max_length=500, blank=True, null=True)
    coat_of_arms_svg = models.URLField(max_length=500, blank=True, null=True)
    borders_with = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.code})'


class Name(models.Model):
    name = models.CharField(max_length=100)
    count_of_reguests = models.IntegerField(default=1)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NameCountryProbability(models.Model):
    name_request = models.ForeignKey(Name, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    probability = models.FloatField()

    class Meta:
        unique_together = ('name_request', 'country')

    def __str__(self):
        return f'{self.name_request} → {self.country} ({self.probability})'
