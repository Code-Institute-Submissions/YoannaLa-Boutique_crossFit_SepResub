from django.shortcuts import redirect, render, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm
from profiles.models import UserProfile


def contact(request):
    print(""" A view to return the contact page """)

    if request.method == "POST":
        print('post')
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            # Send email to customer
            print('valid form')
            cust_email = request.POST['email']
            full_name = request.POST['full_name']
            message = request.POST['message']
            subject = ('We have receiced your message with subject: ' +
                       request.POST['subject'])
            body = render_to_string('contact/confirmation_emails/' +
                                    'customer_confirmation_email.txt',
                                    {'full_name': full_name,
                                        'subject': subject,
                                        'message': message,
                                     })

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email],
                fail_silently=False,
            )

            # send message to admin
            admin_mail = settings.DEFAULT_FROM_EMAIL
            subject = contact_form.cleaned_data['subject']
            body = render_to_string('contact/confirmation_emails/' +
                                    'admin_confirmation_email.txt',
                                    {'full_name': full_name,
                                        'subject': subject,
                                        'message': message,
                                        'cust_email': cust_email,
                                     })

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [admin_mail],
                fail_silently=False,
            )
            # save message to database
            contact_form.save()

            messages.success(request, 'Your message was sent successfully!')
            return redirect(reverse('contact_success'))
        else:
            messages.error(request, 'Failed to send message. \
                Please ensure the form is valid.')
            print('not valid')
    else:
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            try:
                contact_form = ContactForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'subject': '',
                    'message': '',
                })

            except UserProfile.DoesNotExist:
                contact_form = ContactForm()
        else:
            contact_form = ContactForm()

        context = {
            'form': contact_form,
            'on_profile_page': True,
        }

    return render(request, 'contact/contact.html', context)



def contact_success(request):

    return render(request, 'contact/contact_success.html')
