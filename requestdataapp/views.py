from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm
import os


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    saved_file_url = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #myfile = request.FILES["myfile"]
            myfile = form.cleaned_data["file"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            saved_file_url = fs.url(filename)
            print("saved file", filename)
    else:
        form = UploadFileForm()
    context = {
        "form": form,
        "saved_file_url": saved_file_url,
    }
    return render(request, "requestdataapp/file-upload.html", context=context)


# НОВАЯ ФУНКЦИЯ с ограничением размера файла
def upload_file_with_limit(request: HttpRequest) -> HttpResponse:
    MAX_FILE_SIZE = 1048576  # 1 MB в байтах

    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({'error': 'Файл не предоставлен'}, status=400)

        # Проверка размера файла
        if uploaded_file.size > MAX_FILE_SIZE:
            return JsonResponse({'error': 'Размер файла превышает лимит в 1 МБ'}, status=400)

        # Создаем папку media если её нет
        if not os.path.exists('media'):
            os.makedirs('media')

        # Сохраняем файл
        fs = FileSystemStorage(location='media/')
        filename = fs.save(uploaded_file.name, uploaded_file)

        return JsonResponse({'message': 'Файл успешно загружен', 'filename': filename})

    # Показываем форму для загрузки
    return render(request, "requestdataapp/upload-with-limit.html")
