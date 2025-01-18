from django.shortcuts import render

def my_view(request):
    def my_view(request):
        return render(request, 'index.html', {
            'css_url': '/static/css/styles.css'
        })