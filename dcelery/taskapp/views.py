from django.shortcuts import render,HttpResponse

# Create your views here.
from dcelery.celery import divide  # Assuming 'dcelery' is the module where your Celery app is defined

def home(request):
    # Call the divide task asynchronously with arguments x and y
    result = divide.delay(4, 7)

    # Optionally, you can wait for the result if you need it immediately
    # Note: This will block the execution until the task is complete
    result.wait()

    # You can then retrieve the result using the result.get() method
    print("Result:", result.get())
    return HttpResponse(f"<h1>{result}</h1>")