from django.shortcuts import render, redirect
from .models import Question, Answer
from django.core.paginator import Paginator
from .forms import QuestionForm, AnswerForm
from django.utils import timezone

# Create your views here.

def index(request):
    question_list = Question.objects.all().order_by('-created_at')
    page = request.GET.get('page', '1')
    paginator = Paginator(question_list, 3)
    page_obj = paginator.get_page(page)
    context = {
        'question_list': question_list, 
        'page_obj': page_obj
        }
    return render(request, 'blog/index.html', context)



def detail(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_at = timezone.now()
            answer.save()
            redirect('blog:index')
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'blog/detail.html', context)



def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼에 입력된 값이 유효한지 검사한다. 실패할시 form 에 오류메시지가 저장된다.
            question = form.save(commit=False)
            question.created_at = timezone.now()
            question.save()
            return redirect('blog:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'blog/create_question.html', context)