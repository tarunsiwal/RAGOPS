import os
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from .models import ChatLog, ChatHistory, UploadedFile
from .forms import UserQueryForm, FileUploadForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import uuid 
from .chat_bots import chatbot
from django.contrib.auth.models import User
from django.db.models import Max

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ChatLogSerializer
import PyPDF2


@login_required(login_url='login')
def base(request):
    return render(request, 'base.html',{})

@login_required(login_url='login')
def choose_llm(request):
    return render(request, 'select-llm-model.html',{})

@login_required(login_url='login')
def vector_storing(request):
    return render(request, 'vector-storing.html',{})

@login_required(login_url='login')
def get_API(request):
    return render(request, 'get-API.html',{})

@login_required(login_url='login')
def data_connect(request):
    return render(request, 'data-connection.html',{})

@login_required(login_url='login')
def chat_screen_temp(request):
    return render(request, 'chat-screen-temp.html',{})

@login_required(login_url='login')
def prompt_screen(request):
    return render(request, 'prompt-screen.html',{})

@login_required(login_url='login')
def track_query(request):
    chat_id = request.session.get('chat_id')
    count = ChatLog.objects.filter(user=request.user, chat_id=chat_id).count()
    pricing = count*0.40
    chat_history = ChatHistory.objects.get(chat_id=chat_id, user=request.user)
    chat_history.pricing = pricing
    chat_history.save()

    return render(request, 'track-query.html',{'pricing':pricing, 'count':count})
 
@login_required(login_url='login')
def chat_history(request):
    chat_histories = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chat-history.html', {'chat_histories': chat_histories})

def delete_chat_history(request, chat_id):
    # Assuming you have user information available in the request
    user = request.user
    chat_history = get_object_or_404(ChatHistory, chat_id=chat_id, user=user)
    chat_history.delete()

    return redirect('chat_history')

@login_required(login_url='login')
def new_chat(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        chat_id = f"{request.user.id}${uuid.uuid1()}"
        ChatHistory.objects.create(user = user, chat_id = chat_id, chat_name = 'United chat') #, prompt = prompt)
        chat_history = ChatHistory.objects.get(chat_id=chat_id, user=request.user)
        ai_response = call_chatbot.chatbot_interface('', '', '')
        # ai_response = get_ai_response(None, None, '')
        prompt = ai_response['prompt']
        chat_history.prompt = prompt
        chat_history.save()

        request.session['chat_id'] = chat_id
        return redirect('chat_screen')

    return render(request, 'chat-screen.html', {'chat_history': {}, 'latest_prompt': ''})

@login_required(login_url='login')
def chat_screen(request):

    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        form = UserQueryForm(request.POST)
        chat_id = request.session.get('chat_id')
        uploaded_files = UploadedFile.objects.filter(user=request.user, chat_history__chat_id = chat_id)
        
        if form.is_valid() and uploaded_files:
            user_query = form.cleaned_data['user_query']
            file_paths = request.session.get('file_paths')
            chat_id = request.session.get('chat_id')
            first_chat_log = ChatLog.objects.filter(user=request.user, chat_id=chat_id).order_by('timestamp').first()
            chat_history = ChatHistory.objects.get(chat_id=chat_id, user=request.user)

            if first_chat_log:
                user_prompt = first_chat_log.prompt
            elif chat_history.prompt:
                user_prompt = chat_history.prompt
            else:
                user_prompt = ''

            print('before func run',file_paths, '$$$$$$$$$$$$$$$')
            ai_response = call_chatbot.chatbot_interface(user_query, file_paths, user_prompt)
            # ai_response = get_ai_response(user_query, file_paths, user_prompt)
            print(ai_response, 'zzzzzzzzzzzzzzzzzzzzzz')
            # prompt = ai_response['prompt']
            response = ai_response

            ChatLog.objects.create(user = request.user, user_query = user_query, chat_id=chat_id, ai_response = response, prompt = '')

            return redirect('chat_screen')
        else:
            messages.warning(request, 'Please upload document')
    else:
        form = UserQueryForm()

    # Retrieve chat history for the current user
    chat_id = request.session.get('chat_id')
    chat_log = ChatLog.objects.filter(user=request.user, chat_id=chat_id).order_by('-timestamp')
    first_chat_log = chat_log.first()
    uploaded_files = UploadedFile.objects.filter(user=request.user, chat_history__chat_id = chat_id)
    chat_history = ChatHistory.objects.get(chat_id=chat_id, user=request.user)
    uploaded = False

    if chat_log.exists():
        chat_history = ChatHistory.objects.get(chat_id=chat_id, user=request.user)
        prompt = chat_history.prompt
        start_chat = False
        

    elif uploaded_files.exists():
        start_chat = 'How can I help you today?'
        prompt = chat_history.prompt

    else:
        prompt = chat_history.prompt
        start_chat = False
        uploaded = True

    return render(request, 'chat-screen.html', {'form': form, 'chat_log': chat_log, 'latest_prompt': prompt, 'start_chat': start_chat, 'uploaded': uploaded, 'chat_history': chat_history})



@login_required
def update_prompt(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        user = get_object_or_404(User, id=request.user.id)
        chat_id = request.session.get('chat_id')
        first_chat_log = ChatLog.objects.filter(user=user, chat_id=chat_id).order_by('timestamp').first()
        chat_history = ChatHistory.objects.filter(user=user, chat_id=chat_id).order_by('timestamp').first()
        chat_history.prompt = prompt
        chat_history.save()

        if first_chat_log:
            first_chat_log.prompt = prompt
            print('Debug: Updating prompt to', prompt)
            first_chat_log.save()
            messages.success(request, 'Prompt successfully updated!')
        elif chat_history:
            messages.warning(request, 'Prompt successfully updated!')
        else:
            messages.warning(request, 'No entries in ChatLog.')

        return redirect('chat_screen')

    return render(request, 'chat-screen.html')

@login_required(login_url='login')
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            chat_id = request.session.get('chat_id')
            user = request.user
            chat_history = ChatHistory.objects.get(chat_id=chat_id, user=user)
            uploaded_file = form.save(commit=False)
            uploaded_file.user = user
            uploaded_file.chat_history = chat_history
            uploaded_file.save()

            # PDF processing logic
            if uploaded_file.file.name.endswith('.pdf'):
                pdf_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.path)

                # Correct class name
                pdf_reader = PyPDF2.PdfFileReader(pdf_path)
                num_pages = pdf_reader.numPages

                # request.session['pdf_first_page'] = pdf_reader.getPage(0).extractText()
                text = pdf_reader.getPage(0).extractText()
                filename = "untitled.txt"
                with open(filename, "w") as file:
                    file.write(text)
                uploaded_file.file.save(filename, open(filename, "rb"))

                print(uploaded_file)
                print(pdf_reader.getPage(0).extractText())
            else:
                messages.error(request, 'Unsupported file format. Please upload a PDF.')
                return redirect('chat_screen')


            user = get_object_or_404(User, id=request.user.id)
            chat_id = request.session.get('chat_id')
            
            uploaded_files = UploadedFile.objects.filter(user=user, chat_history__chat_id=chat_id)
            file_paths = [uploaded_file.file.path for uploaded_file in uploaded_files]
            absolute_file_paths = [os.path.join(settings.MEDIA_ROOT, path) for path in file_paths]
            # Store the array in the session
            request.session['file_paths'] = absolute_file_paths

            messages.success(request, 'File uploaded successfully!')
            return redirect('chat_screen')
        else:
            messages.error(request, 'Please enter the a file with correct format - .jpg, .jpeg, .png, .pdf')
            return redirect('chat_screen')

    else:
        form = FileUploadForm()

    return render(request, 'chat-screen.html', {'form': form})

def get_ai_response(user_query, file_paths, user_prompt = ''):
    if user_query != None:
        response = "AI response test: " + user_query
    else:
        response = ''
    if user_prompt == '' or user_prompt == None:
        prompt = "this is the custom prompt"
    else:
        prompt = user_prompt
        
    return {'response_messages': response, 'prompt': prompt, 'file_paths':file_paths}


class call_chatbot:
    def chatbot_interface(query, file_paths, user_prompt = ''):
        if user_prompt:
            prompt = user_prompt
        elif (user_prompt == '' or user_prompt == None):
            prompt = """you are a lawyer assistant chatbot. You have to assist lawyers according to their requirements. 
                            You have to follow each instruction in detail. After reviewing each query, you have to provide an answer to the user.
                            Your main task is to do and compare things according to user questions because this is a large chunk of document.
                            You have to work on this data and provide answers from the document after reviewing all the documents.
                            You have the ability to help lawyers find important things from documents."""

        if query != '' and file_paths != '':
            # prompt=call_chatbot.prompt
            chatbot_instance = chatbot.Chatbot(file_paths, prompt)
            responses = chatbot_instance.respond(query)
            print(responses)
            # response_messages = [f"{document_path}: {response}" for document_path, response in responses]
            response_messages = [response for response in responses]
            # return {'response_messages':"\n".join(response_messages), 'prompt': prompt}
            return "\n".join(response_messages)

        else:
            return {'prompt':prompt}



class ChatLogAPIView(APIView):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return ChatLog.objects.filter(chat_history__user=self.request.user).order_by('-timestamp')

    def get(self, request):
        chat_history = ChatLog.objects.filter(chat_history__user=request.user).order_by('-timestamp')
        serializer = ChatLogSerializer(chat_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = UserQueryForm(request.data)
        if form.is_valid():
            prompt = request.POST.get('prompt')
            user_query = form.cleaned_data['user_query']
            ai_response = get_ai_response(user_query)
            prompt = ai_response['prompt']
            response = ai_response['response']

            chat_id = f"{request.user.id}${uuid.uuid1()}"
            chat_history, created = ChatLog.objects.get_or_create(user=request.user, defaults={'chat_id': chat_id})
            ChatLog.objects.create(chat_history=chat_history, user_query=user_query, ai_response=response, prompt=prompt)

            serializer = ChatLogSerializer(chat_history, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

