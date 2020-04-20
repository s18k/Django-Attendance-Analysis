from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.IntegerField(default=0)
    employee_name=models.CharField(max_length=200)
    employee_email = models.CharField(max_length=50,default="")
    employee_contact=models.IntegerField(default=0)
    employee_position = models.CharField(max_length=50)
    employee_image = models.ImageField(upload_to="analysis/images",default="")

    def __str__(self):
        return (str(self.employee_id)+self.employee_name)

    def getname(self):

        return self.employee_name


class Document(models.Model):
    monthnumber=models.IntegerField(default=1)
    year=models.IntegerField(default=0)
    document=models.FileField(upload_to="analysis/files",default="")

    def __str__(self):
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                  9: "September", 10: "October"
            , 11: "November", 12: "December"}
        s=""
        m=self.monthnumber
        self.month=months[m]
        s+=months[m]
        s+=" "
        s+=str(self.year)
        return (s)

