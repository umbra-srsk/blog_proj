from django.db import models

class MyBoard(models.Model):
    myname = models.CharField(max_length=100)
    mytitle = models.CharField(max_length=500)
    mycontent = models.CharField(max_length=2000)
    mydate = models.DateTimeField()

    def __str__(self):
        return str({'myname': self.myname, 'mytitle': self.mytitle, 'mycontent': self.mycontent, 'mydate': self.mydate})



class MyMember(models.Model):
    myname = models.CharField(max_length=100)
    mypassword = models.CharField(max_length=100)
    myemail = models.CharField(max_length=100)

    def __str__(self):
        return str({'myname': self.myname, 'mypassword': self.mypassword, 'myemail': self.myemail})
    

class Reply(models.Model):
    session_id = models.CharField(max_length=100)
    content = models.TextField(max_length=200)
    dateTime = models.TextField(max_length=100)

    def __str__(self):
        return f"Reply {self.id}"

