from django.apps import AppConfig
import django


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    
    def ready(self) -> None:
       return super().ready()
    
      
            
        
  