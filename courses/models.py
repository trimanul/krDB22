import uuid
from django.db import models
from django.utils import timezone

subjects = [
    ("Математика","Математика"),
    ("Физика","Физика"),
    ("Информатика","Информатика"),
]

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, default="")
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)
    picture = models.ImageField(upload_to="pfps/", default="pfps/default_pfp.png")
    date_created = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"id: {self.id}\nusername: {self.username}\nis_admin: {self.is_admin}\ncreated: {self.date_created}"

    class Meta:
        db_table = 'users'

class Courses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Users, on_delete=models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255)
    subject = models.TextField()
    description = models.TextField(blank=True, null=True)
    difficulty = models.TextField()
    duration = models.TextField()
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    course_pic = models.ImageField(upload_to="course_imgs/", default="course_imgs/default_course_img.png")

    class Meta:
        db_table = 'courses'


class Lists(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'lists'

class Reviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    grade = models.IntegerField()
    author = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        db_table = 'reviews'


class ListsCourses(models.Model):
    list = models.OneToOneField(Lists,  on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lists_courses'
        unique_together = (('list', 'course'),)


class Pages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    html_content = models.TextField()
    page_num = models.IntegerField()

    class Meta:
        db_table = 'pages'

class Tickets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    text = models.TextField()
    class Meta:
        db_table = 'tickets'

class Trackers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    cur_page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    class Meta:
        db_table = 'trackers'
