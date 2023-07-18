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
    
'''
class Reply(models.Model):
    myboard = models.ForeignKey(MyBoard, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    reply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str({'myboard_id': self.myboard_id, 'author': self.author, 'content': self.content, 'reply_date': self.reply_date})
    
'''


class Reply(models.Model):
    myboard = models.ForeignKey(MyBoard, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    reply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str({'myboard_id': self.myboard_id, 'author': self.author, 'content': self.content, 'reply_date': self.reply_date})

