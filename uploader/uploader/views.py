from django.shortcuts import render, redirect, get_object_or_404
# upload files to google drive
import time
from datetime import datetime
import os
import json
import requests
import pywhatkit as pwt
from .Google import Create_Service
from googleapiclient.http import MediaFileUpload
from django.contrib import messages

def uploadFiles(request):
    CLIENT_SECRET_FILE = 'uploader\client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

    # print(dir(service))
    list = []
    list1 = []
    if request.method == 'POST':
        upload_files = request.POST.getlist('upload_files', '')
        # print(upload_files)
        contact_no = request.POST.get('contact_no', '')
        now = datetime.now()

        current_time = now.strftime("%H:%M")
        print("Current Time =", current_time)
        # print(time)
        data = current_time.split(':')
        # print(data)
        hour = data[0]
        # print(hour)
        minute = data[1]
        # print(minute)

        # print(contact_no)
        number = '+91{}'.format(contact_no)
        # print(number)
        # print(upload_files)
        parent_dir = "C:/Users/Dexzter/Downloads/"
        for l in upload_files:
            path = os.path.join(parent_dir, l)
            # print(path)
            file_metadata = {
                'name': l,
                'parents': ['17oCsGSVo-18cnb-EMr4g1IXzX5SokYF3']
            }
            media_content = MediaFileUpload(path, mimetype=None)
            file = service.files().create(
                body=file_metadata,
                media_body=media_content
            ).execute()

            # print(file)
            dict_data = file
            print(dict_data)

            for key, value in dict_data.items():
                list.append(value)
        print(list)
        # for every second element and after 3rd element
        filter_list = list[1::4] 
        print(filter_list)
        for id in filter_list:
            url = " https://drive.google.com/file/d/{}  ".format(id)
            list1.append(url)
        print(list1)
        pwt.sendwhatmsg(number,"Test Reports from Noblestride Fertility and Diagnostic Center, {} Thankyou for visiting us Take Care and Stay Safe".format(list1),int(hour),(int(minute)+2))
        messages.success(request, "Your Message will be send within one minute!")
        return redirect("/")


    else: 
        return render(request, 'uploader/upload_files.html')
