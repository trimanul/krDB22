from django.shortcuts import render, redirect
from django.http import HttpResponse
from courses.models import Courses
from django.forms.models import model_to_dict
from .forms import RegistrationForm, LoginForm, CourseCreationForm, NewReviewForm, ChangeForm, ListCreationForm, TicketCreationForm
from django.contrib import messages
from .models import Users, Reviews, Pages, Lists, ListsCourses, Tickets, Trackers
import bcrypt
from django.core.exceptions import ValidationError
from django.db.models import Avg

from django.conf import settings
import os
import json

def home(request):
    courses = Courses.objects.all()
    if "logged_user" in request.session:
        return render(request, "index.html", {'courses': courses, 'logged_user':request.session["logged_user"]})
    else:
        return render(request, "index.html", {'courses': courses, 'logged_user':0})


def course(request, course_id):
    course = Courses.objects.filter(id=course_id).first()
    reviews = Reviews.objects.filter(course=course).order_by('-date')
    grade_average = reviews.aggregate(Avg('grade'))
    if "logged_user" in request.session:
        return render(request, "course.html", {'course': course, 'reviews':reviews, 'grade_average':grade_average['grade__avg'], 'logged_user':request.session["logged_user"], "course_author":str(course.author.id)})
    else:
        return render(request, "course.html", {'course': course, 'reviews':reviews, 'grade_average':grade_average['grade__avg'], 'logged_user':0, "course_author":str(course.author.id)})

def delete_course(request, course_id):
    course = Courses.objects.filter(id=course_id).first()
    if ("logged_user" in request.session) and (str(course.author.id) == request.session["logged_user"]):
        course.delete()
        messages.success(request, 'Курс успешно удален.')
        return redirect('courses-home')
    else:
        return redirect('courses-home')

def user(request, user_id):
    user = Users.objects.filter(id=user_id).first()
    lists = Lists.objects.filter(user=user)
    if "logged_user" in request.session:
        return render(request, "user.html", {'user': user, 'logged_user':request.session["logged_user"], "lists":lists, "is_admin":user.is_admin})
    else:
        return render(request, "user.html", {'user': user, 'logged_user':0})

def user_delete(request, user_id):
    user = Users.objects.filter(id=user_id).first()
    if ("logged_user" in request.session) and (str(user.id) == request.session["logged_user"]):
        user.delete()
        messages.success(request, 'Пользователь успешно удален.')
        return redirect('courses-logout')
    else:
        return redirect('courses-logout')

def user_change(request, user_id):
    user = Users.objects.filter(id=user_id).first()
    if ("logged_user" in request.session) and (str(user.id) == request.session["logged_user"]):
        if request.method == 'POST':
            form = ChangeForm(request.POST, request.FILES)
            if form.is_valid():
                user.name = request.POST["username"]
                user.email = request.POST["email"]
                user.name = request.POST["name"]
                user.surname = request.POST["surname"]
                user.middle_name = request.POST["middle_name"]
                if (form.cleaned_data["picture"] is not None):
                    user.picture = request.FILES["picture"]
                user.save()
                messages.success(request, 'Аккаунт успешно изменен.')
                return redirect('courses-user', user_id)
        else:
            db_data = {
                "username":user.username,
                "email":user.email,
                "name":user.name,
                "surname":user.surname,
                "middle_name":user.middle_name
            }
            form = ChangeForm(db_data, {"picture":user.picture})
    return render(request, 'change_user.html', {'form': form})

def user_courses(request, user_id):
    courses = Courses.objects.filter(author=user_id)
    if "logged_user" in request.session:
        return render(request, "user_courses.html", {'courses': courses, 'logged_user':request.session["logged_user"]})
    else:
        return render(request, "user_courses.html", {'courses': courses, 'logged_user':0})

def create_course(request, user_id):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        course_author = Users.objects.filter(id=user_id).first()
        if form.is_valid():
            course = None
            if (form.cleaned_data["course_pic"] is not None):
                course = Courses.objects.create(author=course_author, title=form.cleaned_data["title"], subject=form.cleaned_data["subject"], description=form.cleaned_data["description"], difficulty=form.cleaned_data["difficulty"], duration=form.cleaned_data["duration"], course_pic=form.cleaned_data["course_pic"])
            else:
                course = Courses.objects.create(author=course_author, title=form.cleaned_data["title"], subject=form.cleaned_data["subject"], description=form.cleaned_data["description"], difficulty=form.cleaned_data["difficulty"], duration=form.cleaned_data["duration"])
            messages.success(request, 'Курс успешно создан.')
            return redirect('courses-new_page', course.id)
    else:
        form = CourseCreationForm()
        if "logged_user" in request.session:
            return render(request, "course_create.html", {'form': form, 'logged_user':request.session["logged_user"]})
        else:
            return render(request, "course_create.html", {'form': form, 'logged_user':0})

def course_change(request, course_id):
    course = Courses.objects.filter(id=course_id).first()
    if ("logged_user" in request.session) and (str(course.author.id) == request.session["logged_user"]):
        if request.method == 'POST':
            form = CourseCreationForm(request.POST, request.FILES)
            if form.is_valid():
                course.title = request.POST["title"]
                course.subject = request.POST["subject"]
                course.description = request.POST["description"]
                if (form.cleaned_data["course_pic"] is not None):
                    course.course_pic = request.FILES["course_pic"]
                course.save()
                messages.success(request, 'Курс успешно изменен.')
                return redirect('courses-course', course_id)
        else:
            db_data = {
                "title":course.title,
                "subject":course.subject,
                "description":course.description,
            }
            form = CourseCreationForm(db_data, {"course_pic":course.course_pic})
    return render(request, 'change_course.html', {'form': form})

def new_review(request, course_id):
    if request.method == 'POST':
        form = NewReviewForm(request.POST)
        review_author = Users.objects.filter(id=request.session["logged_user"]).first()
        course = Courses.objects.filter(id=course_id).first()
        if form.is_valid():
            Reviews.objects.create(grade=form.cleaned_data["grade"], author=review_author, course=course, text=form.cleaned_data["text"])
            messages.success(request, 'Спасибо за отзыв.')
            return redirect('courses-course', course_id)
    else:
        form = NewReviewForm()
        if "logged_user" in request.session:
            return render(request, "new_review.html", {'form': form, 'logged_user':request.session["logged_user"]})
        else:
            return render(request, "new_review.html", {'form': form, 'logged_user':0})

def new_ticket(request, course_id):
    if request.method == 'POST':
        form = TicketCreationForm(request.POST)
        ticket_author = Users.objects.filter(id=request.session["logged_user"]).first()
        course = Courses.objects.filter(id=course_id).first()
        if form.is_valid():
            Tickets.objects.create(author=ticket_author, course=course, text=form.cleaned_data["text"])
            messages.success(request, 'Спасибо за жалобу.')
            return redirect('courses-course', course_id)
    else:
        form = TicketCreationForm()
        if "logged_user" in request.session:
            return render(request, "new_ticket.html", {'form': form, 'logged_user':request.session["logged_user"]})
        else:
            return render(request, "new_ticket.html", {'form': form, 'logged_user':0, "course":course})

def pages(request, course_id):
    course = Courses.objects.filter(id=course_id).first()
    pages = Pages.objects.filter(course=course).order_by("page_num")
    if "logged_user" in request.session:
        logged_user = Users.objects.filter(id=request.session["logged_user"]).first()
        tracker = Trackers.objects.filter(user=logged_user, course=course).first()
        cur_page = 1
        if (not tracker):
            tracker = Trackers.objects.create(user=logged_user, cur_page=pages.first(), course=course)
            cur_page = tracker.cur_page
        else:
            cur_page = tracker.cur_page
        
        return render(request, "pages.html", {'logged_user':request.session["logged_user"], "pages":pages, "cur_page":cur_page.page_num, "course_id":course_id, "cur_page_id":cur_page.id})
    else:
        return render(request, "pages.html", {'logged_user':0, "pages":pages})
def pages_change_cur(request):
    post = json.loads(request.body)
    user = Users.objects.filter(id=request.session["logged_user"]).first()
    course = Courses.objects.filter(id=post["course_id"]).first()
    cur_page = Pages.objects.filter(course=course, page_num=post["cur_page"]).first()
    tracker = Trackers.objects.filter(user=user, course=course).first()
    tracker.cur_page = cur_page
    tracker.save()
    response_data = {'success':1}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def new_page(request, course_id):
    if request.method == 'POST':
        course = Courses.objects.filter(id=course_id).first()
        print(course.author.id)
        print(request.session["logged_user"])
        if ("logged_user" in request.session) and (str(course.author.id) == request.session["logged_user"]):
            vals = {i:i for i in request.POST["order"].split(" ")[1:]}
            for k in vals.keys():
                if k in request.POST.keys():
                    vals[k] = request.POST[k]

            for k in vals.keys():
                if k in request.FILES.keys():
                    vals[k] = request.FILES[k].name
            for (_, file) in request.FILES.dict().items():
                print(os.path.join(settings.BASE_DIR, 'courses/media') + file.name)
                with open(settings.MEDIA_ROOT + '/page_imgs/' + file.name, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            
            html = ""
            for tag, val in vals.items():
                if "img" in tag:
                    html = html + f'<img src="/media/page_imgs/{val}">\n'
                else:
                    html = html + f'<p>{val}</p>\n'
            prev_pages = Pages.objects.filter(course=course).count()
            Pages.objects.create(course=course, html_content = html, page_num=(prev_pages + 1))
            messages.success(request, 'Страница добавлена.')
            if bool(request.POST["is_fin"]):
                return redirect(f"/course/{course_id}")
            return render(request, "new_page.html", {'logged_user':request.session["logged_user"]})
        else:
            return redirect("/")
    else:
        if "logged_user" in request.session:
                return render(request, "new_page.html", {'logged_user':request.session["logged_user"]})
        else:
            return redirect("/")

def delete_page(request, course_id, page_id):
    page = Pages.objects.filter(id=page_id).first()
    if ("logged_user" in request.session) and (str(page.course.author.id) == request.session["logged_user"]):
        page.delete()
        messages.success(request, 'Страница успешно удалена.')
        return redirect('courses-pages', course_id)
    else:
        return redirect('courses-pages', course_id)


def list(request, list_id):
    list = Lists.objects.filter(id=list_id).first()
    lists_courses = ListsCourses.objects.filter(list=list)
    print(lists_courses)
    lists_courses = [list_course.course.id for list_course in lists_courses]
    print(lists_courses)
    courses = [Courses.objects.filter(id=course_id).first() for course_id in lists_courses]
    if ("logged_user" in request.session):
        return render(request, "list.html", {'logged_user':request.session["logged_user"], "courses":courses, "list":list})
    else:
        return redirect('courses-home')

def list_create(request):
    courses = Courses.objects.all()
    if request.method == 'POST':
        form = ListCreationForm(request.POST)
        if form.is_valid():
            user = Users.objects.filter(id=request.session["logged_user"]).first()
            list = Lists.objects.create(user=user, title=form.cleaned_data["title"], description=form.cleaned_data["description"])
            course_ids = request.POST["course_list"].split(' ')[1:]
            print(course_ids)
            for id in course_ids:
                course = Courses.objects.filter(id=id).first()
                ListsCourses.objects.create(list=list, course=course)
            messages.success(request, 'Список успешно создан.')
            return redirect('courses-user', request.session["logged_user"])
    else:
        form = ListCreationForm()
    if ("logged_user" in request.session):
        return render(request, "list_create.html", {'logged_user':request.session["logged_user"], "form":form, "courses":courses})
    else:
        return redirect('courses-home')

def admin(request):
    if ("logged_user" in request.session):
        user = Users.objects.filter(id= request.session["logged_user"]).first()
        if user.is_admin:
            users = Users.objects.all()
            courses = Courses.objects.all()
            lists = Lists.objects.all()
            reviews = Reviews.objects.all()

            data = {"logged_user":request.session["logged_user"], 
            "users":users, 
            "courses":courses, 
            "lists":lists, 
            "reviews":reviews,
            }

            return render(request, "admin.html", data)
        else:
            return redirect('courses-home')

def admin_tickets(request):
    tickets = Tickets.objects.all()
    if ("logged_user" in request.session):
        return render(request, "admin_tickets.html", {'logged_user':request.session["logged_user"],"tickets":tickets})
    else:
        return redirect('admin')

def admin_ticket_delete(request, ticket_id):
    ticket = Tickets.objects.filter(id=ticket_id).first()
    ticket.delete()
    messages.success(request, "Жалоба удалена")
    return redirect("courses-admin_tickets")

def signin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан.')
            return redirect('courses-home')
    else:
        form = RegistrationForm()
    return render(request, 'signin.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = Users.objects.filter(username=form.cleaned_data["username"]).first()
            if user:
                if bcrypt.checkpw(form.cleaned_data["password"].encode('utf8'), user.password.encode('utf8')):
                    request.session["logged_user"] = str(user.id)
                    messages.success(request, 'Вы успешно вошли.')
                    return redirect('courses-home')
                
            messages.info(request, 'Неправильное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.session["logged_user"]:
        del request.session["logged_user"]
    return redirect('courses-home')