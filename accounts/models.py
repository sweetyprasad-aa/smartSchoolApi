from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.authtoken.models import Token

# Create your models here.

class UserDetails(models.Model):
    GENDER_CHOICES = (
        ('Female', 'Female',),
        ('Male', 'Male',),
        ('Unsure', 'Unsure',),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserDetails")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/user_profile", blank=True, null=True, default="user.jpeg")
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "UserDetails"
    

@receiver(post_save, sender=User)
def create_auth_token(instance=None, created=False, **kwargs):
    """ create user token """
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_userDetails(instance=None, created=False, **kwargs):
    """ create user profile """
    if created:
        UserDetails.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def sendUserEmail(instance=None, created=False, **kwargs):
#     """ Send email to new user """
#     if created:
#         print(f">---- instance ----> {instance}")
        # if instance.is_active == True :
        #     activation_url = 'http://localhost:8000/set_password/'+str(token)+'/'

        #     subject = 'Reset your password'
        #     mail_body = render_to_string('accounts/email/activation_email.html', {
        #         'user': user,
        #         'activation_url': activation_url,
        #         'logo': 'logo.png',
        #     })

        #     # Send the password reset email to the user's email address
        #     send_mail(subject, '', settings.DEFAULT_EMAIL_FROM, [email], html_message=mail_body)
