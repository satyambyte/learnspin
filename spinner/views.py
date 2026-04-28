import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import LearningList, LearningItem, SpinResult
from .forms import LearningListForm, LearningItemForm, OutcomeForm


def home(request):
    lists = LearningList.objects.all()
    return render(request, 'spinner/home.html', {'lists': lists})


def create_list(request):
    if request.method == 'POST':
        form = LearningListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LearningListForm()
    return render(request, 'spinner/create_list.html', {'form': form})


def list_detail(request, list_id):
    learning_list = get_object_or_404(LearningList, id=list_id)
    items = LearningItem.objects.filter(learning_list=learning_list, is_done=False)
    return render(request, 'spinner/list_detail.html', {
        'learning_list': learning_list,
        'items': items,
    })


def add_item(request, list_id):
    learning_list = get_object_or_404(LearningList, id=list_id)
    if request.method == 'POST':
        form = LearningItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.learning_list = learning_list
            item.save()
            return redirect('list_detail', list_id=list_id)
    else:
        form = LearningItemForm()
    return render(request, 'spinner/add_item.html', {
        'form': form,
        'learning_list': learning_list
    })


def spin(request, list_id):
    learning_list = get_object_or_404(LearningList, id=list_id)
    items = list(LearningItem.objects.filter(
        learning_list=learning_list,
        is_done=False,
        is_active=False
    ))
    if not items:
        return redirect('list_detail', list_id=list_id)
    weights = [item.weight for item in items]
    chosen = random.choices(items, weights=weights, k=1)[0]
    chosen.is_active = True
    chosen.save()
    SpinResult.objects.create(item=chosen, outcome='in_progress')
    return redirect('spin_result', item_id=chosen.id)


def spin_result(request, item_id):
    item = get_object_or_404(LearningItem, id=item_id)
    spin = SpinResult.objects.filter(item=item, outcome='in_progress').last()
    if request.method == 'POST':
        form = OutcomeForm(request.POST, instance=spin)
        if form.is_valid():
            result = form.save()
            if result.outcome == 'completed':
                item.is_done = True
            item.is_active = False
            item.save()
            return redirect('list_detail', list_id=item.learning_list.id)
    else:
        form = OutcomeForm(instance=spin)
    return render(request, 'spinner/spin_result.html', {'item': item, 'form': form})


def history(request):
    results = SpinResult.objects.exclude(outcome='in_progress').order_by('-spun_at')
    return render(request, 'spinner/history.html', {'results': results})