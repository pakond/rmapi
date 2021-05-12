from api.models import Company, Profile, Smartphone, Product, Store, Stock
from api.serializers import CompanySerializer, ProfileSerializer, CustomTokenSerializer, SmartphoneSerializer, ProductSerializer, StoreSerializer, StockSerializer
from api.permissions import IsAdminUser, IsOwner
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response

from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    
    def get_queryset(self):
        company = Company.objects.get(owner=self.request.user)
        stores = Store.objects.filter(company=company)
        stores_ids = []
        for store in stores:
            stores_ids.append(store.id)

        if not self.request.GET.get('product'):
            queryset = Stock.objects.filter(store__in=stores_ids)
            return queryset
        else:
            queryset = Stock.objects.filter(product=self.request.GET.get('product'), store__in=stores_ids)
            return queryset

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated, HasAPIKey]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        company = Company.objects.get(owner=self.request.user)
        if company.type == 'Retailer':
            return Response(data={'detail': 'Retail companies cannot have stocks'}, status=status.HTTP_400_BAD_REQUEST)

        smartphone = Smartphone.objects.get(id=request.POST.get('product'))
        if smartphone:
            if request.POST.get('product_features'):
                product_features = request.POST.get('product_features').split(',')
                if len(product_features) < 2:
                    return Response(data={'detail': 'Smartphone products needed features'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    memory_is_in = False
                    memorys = str(smartphone.memory)
                    memorys = memorys.split(', ')
                    for memory in memorys:
                        if memory == product_features[0]:
                            memory_is_in = True
                            break

                    if (memory_is_in == False):
                        return Response(data={'detail': 'The memory entered in product_features does not match the memory options of this model'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    color_is_in = False
                    colors = str(smartphone.color)
                    colors = colors.split(', ')
                    for color in colors:
                        if color == product_features[1]:
                            color_is_in = True
                            break

                    if (color_is_in == False):
                        return Response(data={'detail': 'The color entered in product_features does not match the color options of this model'}, status=status.HTTP_400_BAD_REQUEST)
                    
            else:
                return Response(data={'detail': 'Smartphone products needed features'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    
    def get_queryset(self):
        company = Company.objects.get(owner=self.request.user)
        queryset = Store.objects.filter(company=company.id)
        return queryset

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated, HasAPIKey]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        company = Company.objects.get(owner=self.request.user)
        serializer.save(company=company)

    def create(self, request, *args, **kwargs):
        company = Company.objects.get(owner=self.request.user)
        if company.type == 'Retailer':
            return Response(data={'detail': 'Retail companies cannot have storehouses'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        company = Company.objects.get(owner=self.request.user)
        stores = Store.objects.filter(company=company.id)
        if len(stores) <= 1:
            return Response(data={'detail': 'At least one storehouse is required'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args,**kwargs)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKey]
    queryset = Product.objects.all()

class SmartphoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Smartphone.objects.all()
    serializer_class = SmartphoneSerializer
    permission_classes = [HasAPIKey]

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.filter(owner=self.request.user)
        return queryset
 
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated, HasAPIKey]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if Company.objects.filter(owner=self.request.user).exists():
            return Response(data={'detail': 'This user already has a company'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.POST.get('type') == 'Retailer' and request.POST.get('dropshipping') == 'true':
                return Response(data={'detail': 'Retail companies cannot offer dropshipping'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        if request.POST.get('type') == 'Retailer' and request.POST.get('dropshipping') == 'true':
            return Response(data={'detail': 'Retail companies cannot offer dropshipping'}, status=status.HTTP_400_BAD_REQUEST)

        return self.partial_update(request, *args, **kwargs)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated, HasAPIKey]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsOwner, HasAPIKey]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if Profile.objects.filter(owner=self.request.user).exists():
            return Response(data={'detail': 'This user already has a profile'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            #'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}/reset_password/{}".format(settings.SITE_URL, reset_password_token.key),
            'site_name': settings.SITE_NAME,
            'site_domain': settings.SITE_URL
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {}".format(settings.SITE_FULL_NAME),
            # message:
            email_plaintext_message,
            # from:
            "noreply@{}".format(settings.SITE_URL),
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = (HasAPIKey,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_400_BAD_REQUEST)

        # check if user has password to change
        if not reset_password_token.user.has_usable_password():
            return Response({'status': 'irrelevant'})

        return Response({'status': 'OK'})