"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    try :
        subject=request.POST['subject']
    except:
        subject='null'
    latest_question_list = Question.objects.order_by('-pub_date')
    subjects = Question.objects.values_list('subject',flat=True).distinct()
    template = loader.get_template('polls/index.html')
    
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'subjects':subjects,
                'subject':subject,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id,choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice= get_object_or_404(Choice, pk=choice_id)
    good=''
    bad=''
    if(choice.correct==True):
        good='Good Answer'
    else:
        bad='bad Answer'
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question,'good':good,'bad':bad})

def results2(request):
    question_id=request.POST.get('question_id')
    choice_id=request.POST.get('choice_id')
    print(choice_id)
    choice= get_object_or_404(Choice, pk=choice_id)
    re=3
    if(choice.correct==True):
         re=1 
    else:
        re=0
    return re
def prueba(request):
    choice_id=request.GET.get('choice_id')
    choice= get_object_or_404(Choice, pk=choice_id)
    ans=0
    if choice.correct==True:
        return JsonResponse({"result": "Good Bro"}, status=200)
    return JsonResponse({"result": "bad Answer"}, status=200)

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': get_object_or_404(Choice, pk=username)
    }
    return data
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,selected_choice.id,)))

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        question = Question.objects.get(id = question_id)
        choices = Choice.objects.filter(question=question_id)
        counter = count(choices)
        correctCounter = count(choices.filter(correct=True))
       
        msg=''
        if request.method =='POST' and counter<4 :
            form = ChoiceForm(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = question
                choice.vote = 0
                if counter<3 :
                    if not(choice.correct==True and correctCounter==1) :
                        choice.save()
                        msg='Question added'
                    else :
                        msg='There can only one Good Answer'
                else:
                    if (choice.correct==True and correctCounter==0 or choice.correct==False and correctCounter==1):
                        choice.save()
                        msg='Answer added'
                    else:
                        if correctCounter==0 :
                            msg='You must enter a Answer'
                        else:
                            msg='There can only One Good Answer'
                #form.save()
        else: 
            if counter>=4 :
                msg='There are more than 4 options'
               
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form,'message': msg})

def count(i):
    c = 0
    for l in i: c += 1
    return c
def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)


def delete_data(request,question_id):
    if request.method=='POST':
        question = Question.objects.get(id = question_id)
        question.delete()
        return HttpResponseRedirect('/polls/')