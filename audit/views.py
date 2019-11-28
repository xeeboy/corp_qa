from django.shortcuts import render
from .models import AuditTopic, Entry
from dw_query.models import UnPass
from .forms import TopicForm, EntryForm
from dw_query.forms import ParseUp
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def topics(request, unpass_id):
    unpass = UnPass.objects.get(id=unpass_id)
    form = ParseUp(instance=unpass)
    topics = unpass.audittopic_set.order_by('date_added')
    context = {'topics': topics, 'unpass_id': unpass_id, 'form': form}
    return render(request, 'audit/topics.html', context=context)


@login_required
def new_topic(request, unpass_id):
    if request.method != 'POST':
        # if user don't post data, create a new one.
        form = TopicForm()
    else:
        # if user post data, parse data.
        form = TopicForm(data=request.POST, files=request.FILES)  # 要想实现文件上传, 必须传入files
        if form.is_valid():
            _new_topic = form.save(commit=False)
            _new_topic.unpass_id = unpass_id
            _new_topic.from_user = request.user
            _new_topic.save()
            return HttpResponseRedirect(reverse('audit:topics', args=[unpass_id]))
    context = {'unpass_id': unpass_id, 'form': form}
    return render(request, 'audit/new_topic.html', context)


@login_required
def follow(request, topic_id):
    """
    follow actually is entries show for each audit_topic,
    html will add a button behind for adding new entry.
    """
    topic = AuditTopic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')
    context = {'entries': entries, 'topic_id': topic_id}
    return render(request, 'audit/follow.html', context=context)


@login_required
def new_entry(request, topic_id):
    if request.method != 'POST':
        # if user don't post data, create a new one.
        form = EntryForm()
    else:
        # if user post data, parse data.
        form = EntryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            _new_entry = form.save(commit=False)
            _new_entry.topic_id = topic_id
            _new_entry.from_part = request.user
            _new_entry.save()
            return HttpResponseRedirect(reverse('audit:follow', args=[topic_id]))
    context = {'topic_id': topic_id, 'form': form}
    return render(request, 'audit/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic_id = entry.topic_id
    if request.method != 'POST':
        print(request.GET)
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('audit:follow', args=[topic_id]))
    context = {'form': form, 'entry': entry}
    return render(request, 'audit/edit_entry.html', context=context)


@login_required
def del_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    return HttpResponseRedirect(reverse('audit:follow', args=[entry.topic_id]))
