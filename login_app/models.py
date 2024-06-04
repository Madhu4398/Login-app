from django.db import models

# Create your models here.
# Column name in table with thier type
class Register_user(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    pwd_strength = models.CharField(max_length=10)
    pwd_date = models.CharField(max_length=10)
    

    class Meta:
        # Table creation
        db_table = "user_data"
    
    

  
