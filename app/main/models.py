from django.db import models

# Create your models here.
class Sonarqube(models.Model):
    full_version = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.full_version
    
class Plugin(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100, default="Unknown language")
                                                       
    
    def __str__(self):
        if self.language=="Unknown language":
            return self.name
        else:
            return self.language
    
class Compatibility(models.Model):
    class Meta:
        verbose_name_plural = "compatibilities"

    sonarqube = models.ForeignKey(Sonarqube, null=False, on_delete=models.CASCADE)
    plugin = models.ForeignKey(Plugin, null=False,  on_delete=models.CASCADE)
    version = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.plugin.name}-{self.version} for {self.sonarqube.full_version}'