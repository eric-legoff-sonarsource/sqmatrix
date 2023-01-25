from django.apps import AppConfig
from settings import project
import requests
import re
import base64
import os



class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    
    def ready(self) -> None:
        
        for v in project.SQ_VERSIONS:
            file_content = get_gradle_config(v)
            jars = jar_list(file_content)
            #print(len(jars))
            for jar in jars:
                print("{0} => {1}".format(v,jar))
            print('=======\n\n')
        return super().ready()
    
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

def jar_list(filecontent):
    ''' Returns the list of Sonarsource jar files 
    in the given gradle file'''
    
    result = []
    lines =  filecontent.split('\n')
    
    regexp = '^.*dependency\s+\'(com|org)\.sonar.*?\:(.*[0-9]+)\'$'
    
    for line in lines:
        res = re.search(regexp, line)
        if res:
            if len(res.groups()) == 2:
                result.append(res.group(2).split(':'))
            
    return result        
            
        
  