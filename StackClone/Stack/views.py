from django.shortcuts import render,redirect
from Stack.forms import LoginForm,RegistrationForm,QuestionForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from Stack.models import Answers,Questions
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"u must login to perform this process")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


@method_decorator(signin_required,name="dispatch")
class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})


decorators=[signin_required,never_cache]

@method_decorator(decorators,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("home")
    context_object_name="questions"


    def form_valid(self,form):
        form.instance.user=self.request.user
        # messages.success(self.request,"todo hasbeen created")
        return super().form_valid(form)

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)
@signin_required
def add_answer(request,*args,**kwargs):
    question_id=kwargs.get("id")
    ques=Questions.objects.get(id=question_id)
    ans=request.POST.get("answer")
    ques.answers_set.create(answer=ans,user=request.user)
    return redirect("home")

@signin_required
def upvote_view(request,args,*kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    return redirect("home")


@signin_required
def remove_answer(request,*args,**kwargs):
    ans=kwargs.get("id")
    Answers.objects.get(id=ans,)


@signin_required
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class MyQuestionsView(ListView):
    model=Questions
    context_object_name="questions"
    template_name="myquestions.html"

    def get_queryset(self):
        return Questions.objects.filter(user=self.request.user)