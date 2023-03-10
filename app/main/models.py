from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import re
import base64
import os

LANGUAGES = {
    "sonar-abap" : "ABAP",
    "sonar-css" : "CSS",
    "sonar-text" : "Text",
    "sonar-json" : "JSON",
    "sonar-xml" : "XML",
    "sonar-python" : "Python",
    "sonar-apex" : "Apex",
    "sonar-html" : "HTML",
    "sonar-tsql" : "TSQL",
    "sonar-vb"  : "VB",
    "sonar-iac" : "IaC",
    "sonar-scala" : "Scala",
    "sonar-go" : "Go",
    "sonar-php" : "PHP",
    "sonar-javascript" : "Javascript",
    "sonar-java" : "Java",
    "sonar-flex" : "Flex",
    "sonar-vbnet" : "VbNet",
    "sonar-csharp" : "C#",
    "sonar-swift" : "Swift",
    "sonar-rpg" : "RPG",
    "sonar-pli" : "PL1",
    "sonar-cfamily" : "C",
    "sonar-cobol" : "COBOL"    
}

UNKNOWN="Unknown language"
# Create your models here.
class Sonarqube(models.Model):
    full_version = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.full_version
    
    def save(self, *args, **kwargs):
        super(Sonarqube, self).save(*args, **kwargs)
        
    def __lt__(self, other):
        major, minor, patch, build = self.full_version.split('.')
        other_major, other_minor, other_patch, other_build = other.full_version.split('.')
    
        if int(major) < int(other_major):
            return True
        elif int(major) > int(other_major):
            return False
        
        if int(minor) < int(other_minor):
            return True
        elif int(minor) > int(other_minor):
            return False
        
        if int(patch) < int(other_patch):
            return True
        elif int(patch) > int(other_patch):
            return False
        
        if  int(build) < int(other_build):
            return True
        elif int(build) > int(other_build):
            return False
        
        return False
        
        
        
        
    
    
class Plugin(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100, default=UNKNOWN)
                                                       
    
    def __str__(self):
        if self.language==UNKNOWN:
            return self.name
        else:
            return self.language
        
    def __lt__(self, other):
        return self.name < other.name
    
class Compatibility(models.Model):
    class Meta:
        verbose_name_plural = "compatibilities"

    sonarqube = models.ForeignKey(Sonarqube, null=False, on_delete=models.CASCADE)
    plugin = models.ForeignKey(Plugin, null=False,  on_delete=models.CASCADE)
    version = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.plugin.name} v{self.version}'
    
    def __lt__(self, other):
        if self.sonarqube < other.sonarqube:
            return True
        elif self.sonarqube > other.sonarqube:
            return False
        
        if self.plugin.name < other.plugin.name:
            return True
        elif self.plugin.name > other.plugin.name:
            return False
        
        major, minor, patch, build = self.version.split('.')
        other_major, other_minor, other_patch, other_build = other.version.split('.')
        
        if int(major) < int(other_major):
            return True
        elif int(major) > int(other_major):
            return False
        
        if int(minor) < int(other_minor):
            return True
        elif int(minor) > int(other_minor):
            return False
        
        if int(patch) < int(other_patch):
            return True
        elif int(patch) > int(other_patch):
            return False
        
        if  int(build) < int(other_build):
            return True
        elif int(build) > int(other_build):
            return False
        
        return False
        
        

        
    
    
def get_gradle_config(sqversion):
    '''Provides the raw text content of the build.gradle file 
    of the SonarQube version set as parameter'''
    
    token = os.getenv('SQMATRIX_TOKEN')
    owner = 'SonarSource'
    repo = 'sonar-enterprise'
    path = 'build.gradle?ref={}'.format(sqversion)

    r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=path),
    headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(token),
        'X-GitHub-Api-Version': '2022-11-28'
            }
    )
   
    data = r.json()
    file_content = data.get('content', '')
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()
    
    return file_content

def get_publih_date(sqversion):
    r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}'.format(
    owner=owner, repo=repo, tag=sqversion),
    headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(token),
        'X-GitHub-Api-Version': '2022-11-28'
            }
    )
    data = r.json()
    return data['published_at']

def jar_list(filecontent):
    ''' Returns the list of Sonarsource jar files 
    in the given gradle file'''
    
    result = []
    lines =  filecontent.split('\n')
    
    regexp = '^.*dependency\s+\'(com|org)\.sonar.*?\:(.*\d+)\'$'
    
    
    for line in lines:
        res = re.search(regexp, line)
        if res and len(res.groups()) == 2:
            result.append(res.group(2).split(':'))
    
    return result  
    
# method for updating
@receiver(post_save, sender=Sonarqube, dispatch_uid="fetch_plugins")
def fetch_plugins(sender, instance, **kwargs):
    file_content = get_gradle_config(instance.full_version)
    jars = jar_list(file_content)
    for jar in jars:
        
        plugin_name = jar[0]
        plugin_version = jar[1]
        
        if plugin_name.endswith("plugin"):
            plugin_name = plugin_name[:-7] 
        else:
            continue
        
        l = LANGUAGES.get(plugin_name, UNKNOWN)
        
        Plugin.objects.get_or_create(name=plugin_name, language=l)   
            
        comp = Compatibility(
            sonarqube=instance, 
            plugin=Plugin.objects.filter(name=plugin_name).first(), 
            version=plugin_version)
        comp.save()     