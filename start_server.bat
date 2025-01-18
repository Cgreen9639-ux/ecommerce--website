@echo off
cd /c:/Users/camer/OneDrive/Desktop/Ecommerce website/App
call myenv\Scripts\activate
cd myproject
python ../server.py runserver 8000
