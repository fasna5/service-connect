from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.views.decorators.csrf import csrf_exempt
from . models import User,ServiceProvider
# Create your views here.



@csrf_exempt
def login_view(request):
    user_list=User.objects.values_list('email',flat=True)
    print(user_list)
   
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            # email='kavitha22@gmail.com'
            print(password,"pass")
            print(email,"mail")
            
            if email:
                 user=User.objects.get(email=email)
                 print(user.check_password('12345'))

           
                 user = authenticate(request, username=email, password=password)

                 if user is not None:
                        print("loged inn")
                        return JsonResponse({
                            'status': 'Success',
                            'message': 'Login Success',
                            'email': user.email
                        })
                 else:
                        print("can't login")
                        
                        return JsonResponse({
                            'status': 'Failed',
                            'message': 'Invalid Credentials',
                            # 'users':user_list
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid JSON format'
            })
    return JsonResponse({
        'status': 'Failed',
        'message': 'Invalid request method'
    })


@csrf_exempt
def fetch_service_provider_data(request):
    if request.method=='POST':
      try:
        data=json.loads(request.body)
        id=data.get('id')
        
        if id:
            details=ServiceProvider.objects.get(custom_id=id)
            username=details.user.full_name
            email=details.user.email
            address=details.user.address
            phone=details.user.phone_number
            if details is not None:
                return JsonResponse({
                    'status': 'Success',
                    'message': 'Data Fetched',
                    'Service provider Name':username,
                    'Service provider Email':email,
                    'Address':address,
                    'Phone':phone
                })
            else:
                return JsonResponse({
                    'status': 'Failed',
                    'message':'The Custom ID is not matching'
                })
      except json.JSONDecodeError:
           return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid JSON format'
            })
           
    return JsonResponse({
        'status': 'Failed',
        'message': 'Invalid request method'
    })
