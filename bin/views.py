from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message
from .forms import MessageForm
from django.db.models import Q
from django.urls import reverse

@login_required
def inbox(request):
    conversations = request.user.conversations.all().prefetch_related("participants", "messages")

    conv_list = []
    for conv in conversations:
        other = conv.participants.exclude(pk=request.user.pk).first()
        conv_list.append({
            "conv": conv,
            "other": other
        })

    return render(request, "bin/inbox.html", {
        "conversations": conv_list
    })


@login_required
def search_users(request):
    query = request.GET.get("q", "")
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(pk=request.user.pk)[:10]  # exclude myself, limit results

    return render(request, "bin/search_results.html", {"users": users, "query": query})


@login_required
def conversation_detail(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = conv.messages.select_related('sender').all()

    # mark messages not read by me as read
    unread = messages.exclude(read_by=request.user)
    for m in unread:
        m.read_by.add(request.user)

    # other participant বের করি
    other = conv.participants.exclude(pk=request.user.pk).first()

    form = MessageForm()
    return render(request, 'bin/conversation.html', {
        'conversation': conv,
        'messages': messages,
        'form': form,
        'other': other,   # এখানে পাঠাচ্ছি
    })

@login_required
def start_conversation_with(request, user_id):
    other = get_object_or_404(User, pk=user_id)
    # find existing 1-1 conversation
    conv = Conversation.objects.filter(participants=request.user).filter(participants=other).distinct().first()
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other)
    return redirect('bin_conversation', pk=conv.pk)

@login_required
def send_message(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conv
            msg.sender = request.user
            msg.save()
            # optionally: notify other participants (create notifications)
            return redirect('bin_conversation', pk=conv.pk)
    return redirect('bin_conversation', pk=conv.pk)

@login_required
def delete_conversation(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    if request.method == 'POST':
        conv.delete()
        return redirect('bin_inbox')
    return render(request, 'bin/confirm_delete.html', {'conversation': conv})



# Create your views here.
