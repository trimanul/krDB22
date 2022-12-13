from django import forms
from courses.models import Users, Courses, subjects
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
import bcrypt

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=255)  
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    name = forms.CharField(label="Имя", max_length=255, required=False)
    surname = forms.CharField(label="Фамилия", max_length=255, required=False)  
    middle_name = forms.CharField(label="Отчество", max_length=255, required=False)
    picture = forms.ImageField(label='Изображение', required=False)

  
    def clean_username(self):  
        username = self.cleaned_data['username']
        new = Users.objects.filter(username=username)
        print(new)
        if new.count():  
            raise ValidationError("Пользователь уже существует")  
        return username  
  
    def clean_email(self):  
        email = self.cleaned_data['email']
        new = Users.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Пользователь с данной электронной почтой уже существует.")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Введенные пароли не совпадают")  
        return password2 
  
    def save(self, commit = True):
        password_enc = bcrypt.hashpw(self.cleaned_data['password2'].encode('utf-8'), bcrypt.gensalt()).decode()
        print(self.cleaned_data['picture'])
        if self.cleaned_data['picture'] is not None:
            user = Users.objects.create(email=self.cleaned_data['email'], username=self.cleaned_data['username'], password=password_enc, is_admin=False, name=self.cleaned_data['name'], surname=self.cleaned_data['surname'], middle_name=self.cleaned_data['middle_name'], picture=self.cleaned_data['picture'])  
        else:
            user = Users.objects.create(email=self.cleaned_data['email'], username=self.cleaned_data['username'], password=password_enc, is_admin=False, name=self.cleaned_data['name'], surname=self.cleaned_data['surname'], middle_name=self.cleaned_data['middle_name'])
        return user

class ChangeForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=255)  
    email = forms.EmailField(label='Email')
    name = forms.CharField(label="Имя", max_length=255, required=False)
    surname = forms.CharField(label="Фамилия", max_length=255, required=False)  
    middle_name = forms.CharField(label="Отчество", max_length=255, required=False)
    picture = forms.ImageField(label='Изображение', required=False)

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CourseCreationForm(forms.Form):
    title = forms.CharField(label='Название', min_length=5, max_length=255)
    subject = forms.CharField(label='Предмет', widget=forms.Select(choices=subjects))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea())
    difficulty = forms.CharField(label='Сложность курса', widget=forms.Select(choices=[("Легкий","Легкий"), ("Средний","Средний"), ("Сложный","Сложный")]))
    duration = forms.CharField(label='Длительность курса')
    course_pic = forms.ImageField(label='Изображение', required=False)

class ListCreationForm(forms.Form):
    title = forms.CharField(label='Название', min_length=5, max_length=255)
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea())

class NewReviewForm(forms.Form):
    grade = forms.IntegerField(label='Оценка', widget=forms.Select(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)]))
    text = forms.CharField(label='Текст', required=False, widget=forms.Textarea())

class TicketCreationForm(forms.Form):
    text = forms.CharField(label='Текст жалобы',widget=forms.Textarea)