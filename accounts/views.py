from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.auth import authenticate, logout, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from accounts.models import UserDetails

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login_view(request):
    for i in request.data:
        print(i, request.data[i])
    username = request.data['username'].strip()
    password = request.data['password'].strip()

    if User.objects.filter(username=username).exists():
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user) 
            return Response({'status': 'success', 'message': 'Login successfully.', 'token':token.key},status=status.HTTP_200_OK)
        else:
            return Response({'status': 'success', 'message': 'Password dose not match, please try again.'},status=status.HTTP_200_OK)
    else:
        return Response({'status': 'success', 'message': 'Entered email-id is not register, please check and try again.'},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def logout_view(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({'status': 'success', 'message': 'Logout successfully.'},status=status.HTTP_200_OK)
    except:
        return Response({'status': 'success', 'message': 'Somthing went wrong, please login and try again.'},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup_view(request):
    if 'username' not in request.data:
        return Response({'status': 'success',
                         'message': 'Username is mandatory field.'}
                         ,status=status.HTTP_200_OK)
    
    if 'password' not in request.data or 'confirm_password' not in request.data:
        return Response({'status': 'success',
                         'message': 'Password and confirm-password are mandatory fields.'}
                         ,status=status.HTTP_200_OK)
    
    if request.data['password'] != request.data['confirm_password']:
        return Response({'status': 'success',
                         'message': 'Password and confirm-password must be same.'}
                         ,status=status.HTTP_200_OK)
    
    user_data_key_list = ['username', 'first_name', 'last_name', 'email','password']
    user_data = {}

    for key in request.data:
        if key in user_data_key_list:
            user_data[key]= request.data[key]

    User.objects.create_user(**user_data)

    return Response({'status': 'success', 'message': 'User register successfully.'},status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user_profile_view(request):

    if 'first_name' not in request.data:
        return Response({'status': 'success',
                        'message': 'Please enter your first name'}
                        ,status=status.HTTP_200_OK)

    if 'last_name' not in request.data:
        return Response({'status': 'success',
                        'message': 'Please enter your last name'}
                        ,status=status.HTTP_200_OK)

    if 'email' not in request.data:
        return Response({'status': 'success',
                        'message': 'Please enter your email'}
                        ,status=status.HTTP_200_OK)

    if 'gender' not in request.data:
        return Response({'status': 'success',
                        'message': 'Please select gender'}
                        ,status=status.HTTP_200_OK)
    if 'DOB' not in request.data:
        return Response({'status': 'success',
                        'message': 'Please enter your date-of-birth'}
                        ,status=status.HTTP_200_OK)
    if 'profile_image' not in request.FILES:
        return Response({'status': 'success',
                        'message': 'Please upload your profile picture.'}
                        ,status=status.HTTP_200_OK)
    
    gender = request.data['gender'].capitalize() 
    DOB = request.data['DOB']
    profile_image = request.FILES['profile_image']

    user_profile = UserDetails.objects.filter(user= request.user)
    if user_profile is not None:
        User.objects.filter(username = request.user.username).update(first_name = request.data['first_name'],
                                                                     last_name = request.data['last_name'],
                                                                     email=request.data['email'])
        
        user_profile.update(gender= gender, date_of_birth = DOB, profile_image=profile_image)
        updated_user_details = User.objects.filter(username = request.user.username).values('username',
                                                                                            'email',
                                                                                            'first_name',
                                                                                            'last_name',
                                                                                            'UserDetails__gender',
                                                                                            'UserDetails__date_of_birth',
                                                                                            'UserDetails__profile_image')
        return Response({'status': 'success',
                            'message': 'Profile Update successfully.',
                            'user_details':updated_user_details},status=status.HTTP_200_OK)
    else:
        return Response({'status': 'success', 'message': 'Somthing went wrong, please login and try again.'},status=status.HTTP_200_OK)
    
@api_view(['GET'])
def user_profile_view(request):
    updated_user_details = User.objects.filter(username = request.user.username).values('username',
                                                                                        'email',
                                                                                        'first_name',
                                                                                        'last_name',
                                                                                        'UserDetails__gender',
                                                                                        'UserDetails__date_of_birth',
                                                                                        'UserDetails__profile_image')
    return Response({'status': 'success',
                             'message': 'Profile Update successfully.',
                             'user_details':updated_user_details},status=status.HTTP_200_OK)

@api_view(['POST'])
def change_password_view(request):
    if 'current_password' not in request.data:
        return Response({'status': 'success',
                         'message': 'Plesae enter your current password.'},status=status.HTTP_200_OK)
    
    if 'new_password' not in request.data:
        return Response({'status': 'success',
                            'message': 'Plesae enter your new password.'},status=status.HTTP_200_OK)
    if 'confirm_password' not in request.data:
        return Response({'status': 'success',
                         'message': 'Plesae enter your confirm password.'},status=status.HTTP_200_OK)
    
    current_password = request.data['current_password']
    new_password = request.data['new_password']
    confirm_password = request.data['confirm_password']

    if new_password != confirm_password:
        return Response({'status': 'success',
                         'message': 'New password and confirm password must same.'},status=status.HTTP_200_OK)
    try:
        user = authenticate(username=request.user.username, password = current_password )
        if user.check_password(new_password):
            return Response({'status': 'success',
                            'message': 'You are using your old password as new password, please try somthing different.'},status=status.HTTP_200_OK)
        user.set_password(new_password)
        Token.objects.filter(user=user).delete()
        user.save()
        return Response({'status': 'success',
                         'message': 'Password successfully change, plese login again.'},status=status.HTTP_200_OK)
    except:
        return Response({'status': 'success',
                         'message': 'Somthing went wrong, please login and try again.'},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def forgot_password_view(request):
    if 'email' not in request.data:
        return Response({'status':'success',
                            'message':'Please enter your email'},status=status.HTTP_200_OK)
    if not User.objects.filter(email=request.data['email']).exists():
        return Response({'status':'success',
                            'message':'This emial does not exists.'},status=status.HTTP_200_OK)
    try:
        user = User.objects.get(email=request.data['email'])
        token, current = Token.objects.get_or_create(user=user)
    except:
        return Response({'status': 'success',
                                'message': 'Somthing went wrong, please login and try again.'},status=status.HTTP_200_OK)

    reset_url = settings.DOMAIN + '/api/setPassword/?token='+str(token.key) 
    print(reset_url)
    subject = 'Reset your password'
    mail_body = render_to_string('email/reset_password_email.html', {
        'user': user,
        'reset_url': reset_url,
        'logo': 'logo.png',
    })

    # Send the password reset email to the user's email address
    send_mail(subject, '', settings.DEFAULT_EMAIL_FROM, [request.data['email']], html_message=mail_body)
    return Response({'status':'success',
                     'message':'Reset Password link send to your email.'},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def set_password_view(request):
    token = request.query_params.get('token')
    print(token, '>------------------> Hello')
    # if 'token' not in request.data:
    #     return Response({'status': 'success',
    #                         'message': 'Plesae enter your token.'},status=status.HTTP_200_OK)
    if 'new_password' not in request.data or request.data['new_password'].strip() == '':
        return Response({'status': 'success',
                            'message': 'Plesae enter your new password.'},status=status.HTTP_200_OK)
    if 'confirm_password' not in request.data or request.data['confirm_password'].strip() == '':
        return Response({'status': 'success',
                         'message': 'Plesae enter your confirm password.'},status=status.HTTP_200_OK)
    # token = request.data['token']
    new_password = request.data['new_password']
    confirm_password=request.data['confirm_password']
    if new_password != confirm_password:
            return Response({'status': 'success',
                         'message': 'New password and confirm password must same.'},status=status.HTTP_200_OK)
    try:
        user = User.objects.get(auth_token=token)
        user.set_password(new_password)
        user.save()
        Token.objects.filter(key=token).delete()
        return Response({'status':'success',
                         'message':'Password set successfully, please login again'},status=status.HTTP_200_OK)
    except:
        return Response({'status':'success',
                         'message':'Link Expire, please try again'},status=status.HTTP_200_OK)
    
    