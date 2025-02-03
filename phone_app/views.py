from django.shortcuts import render
from .utils import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_application(request):
    message = None  # To hold success or error messages
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Retrieve the validated data
            aName = form.cleaned_data['aName']
            aCategory = form.cleaned_data['aCategory']
            aSize = form.cleaned_data['aSize']
            # Create the new Application with isInstalled set to 0.
            Applications.objects.create(
                aname=aName,
                acategory=aCategory,
                asize=aSize,
                isinstalled=0
            )
            message = "Application added successfully."
            form = ApplicationForm()  # Reset form after successful submission.
        else:
            # Aggregate error messages from the form.
            error_list = []
            for field, errors in form.errors.items():
                error_list.append(f"{field}: {', '.join(errors)}")
            message = "Error(s): " + " | ".join(error_list)
    else:
        form = ApplicationForm()
    return render(request, 'add_application.html', {'form': form, 'message': message})

def remove_application(request):
    message = None
    available_space = get_available_space()

    if request.method == 'POST':
        form = RemoveApplicationForm(request.POST)
        if form.is_valid():
            app_name = form.cleaned_data['app']
            try:
                # Retrieve the selected application (which must be installed)
                app_obj = Applications.objects.get(aname=app_name)
            except Applications.DoesNotExist:
                message = "Selected application does not exist."
                form = RemoveApplicationForm()  # reinitialize the form
            else:
                # "Remove" the app by setting isinstalled to 0
                app_obj.isinstalled = 0
                app_obj.save()
                message = f"{app_name} removed successfully."
                available_space = get_available_space()
                # Reinitialize the form so that it only shows apps still installed.
                form = RemoveApplicationForm()
        else:
            message = "Invalid form submission."
    else:
        form = RemoveApplicationForm()

    return render(request, 'remove_application.html', {
        'form': form,
        'message': message,
        'available_space': available_space,
    })

def install_application(request):
    message = None
    available_space = get_available_space()

    if request.method == 'POST':
        form = InstallApplicationForm(request.POST)
        if form.is_valid():
            app_name = form.cleaned_data['app']
            try:
                # Retrieve the chosen application
                app_obj = Applications.objects.get(aname=app_name)
            except Applications.DoesNotExist:
                message = "Selected application does not exist."
                form = InstallApplicationForm()  # reinitialize form
            else:
                # Calculate the new used space if this app is installed.
                current_used = Applications.objects.filter(isinstalled=1).aggregate(total=Sum('asize'))[
                                   'total'] or 0
                new_used = current_used + app_obj.asize

                if new_used > 1800:
                    message = f"Error: Installing {app_name} would exceed available space."
                else:
                    # Mark the app as installed.
                    app_obj.isinstalled = 1
                    app_obj.save()
                    message = f"{app_name} installed successfully."
                    # Update available space after installation.
                    available_space = get_available_space()
                    # Reinitialize the form so the installed app no longer appears.
                    form = InstallApplicationForm()
        else:
            message = "Invalid form submission."
    else:
        form = InstallApplicationForm()

    return render(request, 'install_application.html', {
        'form': form,
        'message': message,
        'available_space': available_space,
    })

def query_results(request):
    queries = {
        'query1': query1(),
        'query2': query2(),
        'query3': query3()
    }
    return render(request, 'query_results.html', queries)