from django.http import JsonResponse

from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token

from .serializers import *

class SignUpView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        # checking user already exists
        valid_email = User.objects.filter(email__iexact=request.data['email'])
        if valid_email:
            return JsonResponse('already created' , safe=False)
        else:
            try:    
                data = request.data
                data['username'] = data['email']
                # pass data to the serializer for validating 
                serializer = UserSerializer(data=data)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    # create the user
                    user = serializer.save()
                    try:
                        # activate the user
                        if user.is_active == False:
                            user.is_active=True
                            user.save()
                        return JsonResponse('Your account has been activated successfully, please login and check.', safe=False)
                    except:
                        return JsonResponse('Signup failed ' , safe=False)
                else:                    
                    return JsonResponse('Invalid request or field missing!' , safe=False)
            except KeyError:
                return JsonResponse('Invalid request or field missing!' , safe=False)
            

class LoginView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        login_serializer = UserLoginSerializer(data=data)   

        # Pass data to the serializer to validate 
        if login_serializer.is_valid():
            email=data['email']
            password=data['password']
            # Check email already exists or not
            valid_email = User.objects.filter(email__iexact=data['email'])
            if valid_email:
                # Check user active status
                check_to_active_email = User.objects.filter(email__iexact=data['email'],is_active = True)
                if check_to_active_email:
                    # check authentication 
                    request_user = login_serializer.authenticate(email=email,password=password)
                    if request_user:
                        try:
                            Token.objects.get(user=request_user).delete()
                        except Exception as er:
                            pass
                        Token.objects.create(user=request_user)
                        new_token = list(Token.objects.filter(user_id=request_user).values("key"))  
                        msg={
                            "token":str(new_token[0]['key']),
                            'username':str(request_user),
                            'email':request_user.email,
                            'user_id':request_user.id,
                            'first_name': request_user.first_name,
                            'last_name': request_user.last_name,
                        }
                        return JsonResponse(msg , safe=False)
                    else:
                        return JsonResponse('Please check your password again.' , safe=False)
                else:
                    return JsonResponse('Your email id not registered or temporary blocked.' , safe=False)
            else:
                return JsonResponse('Email not activate' , safe=False)
        else:
            return JsonResponse('Your email id is not registered. Please signup to activate your account.' , safe=False)