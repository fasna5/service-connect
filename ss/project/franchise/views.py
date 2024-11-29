from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from franchise.serializer import ServiceProviderSerializer
from rest_framework import status
from accounts.models import ServiceRegister, Franchisee,ServiceProvider,Ad_Management,Complaint,Dealer,ServiceRequest
from datetime import date, timedelta
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone


# Create your views here.
class FranchiseeStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the logged-in user
        user = request.user
        
        # Get the Franchisee for the logged-in user
        try:
            franchisee = Franchisee.objects.get(user=user)
            print(franchisee)
            user=franchisee.user
            print(user)
        except Franchisee.DoesNotExist:
            return Response({"error": "Franchisee not found for this user"}, status=404)
        
        today = date.today()
        first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
        first_day_of_last_month = first_day_of_last_month.replace(day=1)
        last_day_of_last_month = today.replace(day=1) - timedelta(days=1)

        # Get current date and time
        now = timezone.now()

# Get the first day of the current month
        first_day_of_month = now.replace(day=1)
        
        
        service_count = ServiceRegister.objects.filter(
            service_provider__franchisee__user=user
        ).count()

        service_currentmonth = ServiceRegister.objects.filter(
                           service_provider__franchisee__user=user,
                           created__gte=first_day_of_month,
                           created__lte=now
                           ).count()
        
        service_last_month = ServiceRegister.objects.filter(created__range=
                                [first_day_of_last_month, last_day_of_last_month]
                                ,service_provider__franchisee__user=user).count()
        if (service_currentmonth and service_last_month)==0:
            percentage_difference_service='0%'
        if service_last_month > 0:
            if service_currentmonth >service_last_month:
                percentage_difference_service =f'+{ ((service_currentmonth - service_last_month) / service_last_month) * 100} %'
            else:
                percentage_difference_service =f'{ ((service_currentmonth - service_last_month) / service_last_month) * 100} %'
        
        else:
            percentage_difference_service ='100%'
        

        
        service_providers = ServiceProvider.objects.filter(franchisee=franchisee)
        service_provider_users = service_providers.values_list('user', flat=True)
        
        total_ads_count = 0
    
    # Iterate through all service providers and count their ads
        for serviceprovider in service_providers:
           user = serviceprovider.user
           ads_count = Ad_Management.objects.filter(ad_user=user).count()
           total_ads_count += ads_count  # Add up ads count for each service provider

        ad_currentmonth = Ad_Management.objects.filter(
                           ad_user__in=service_provider_users,
                           valid_from__gte=first_day_of_month,
                           valid_from__lte=now
                           ).count()
        
        
        

        ad_last_month = Ad_Management.objects.filter(valid_from__range=
                                    [first_day_of_last_month, last_day_of_last_month]
                                    ,ad_user__in=service_provider_users).count()
        if (ad_currentmonth and ad_last_month)==0:
            percentage_difference_ad='0%'
        if ad_last_month > 0:
            if ad_currentmonth >ad_last_month:
                percentage_difference_ad =f'+{ ((ad_currentmonth - ad_last_month) / ad_last_month) * 100} %'
            else:
                percentage_difference_ad =f'{ ((ad_currentmonth - ad_last_month) / ad_last_month) * 100} %'
        
        else:
            percentage_difference_ad ='100%'
        
        

        
        
        total_complaints_count=0
        for service_provider in service_providers:
           user = service_provider.user
           complaints_count = Complaint.objects.filter(service_request__service_provider=user).count()
           total_complaints_count += complaints_count  # Add up ads count for each service provider

        complaint_currentmonth = Complaint.objects.filter(
                           sender__in=service_provider_users,
                           submitted_at__gte=first_day_of_month,
                           submitted_at__lte=now
                           ).count()+Complaint.objects.filter(
                           receiver__in=service_provider_users,
                           submitted_at__gte=first_day_of_month,
                           submitted_at__lte=now
                           ).count()

        
        complaint_last_month = Complaint.objects.filter(submitted_at__range=[first_day_of_last_month, last_day_of_last_month],
                       sender__in=service_provider_users
                       ).count() + Complaint.objects.filter(
                       submitted_at__range=[first_day_of_last_month, last_day_of_last_month],
                       receiver__in=service_provider_users
                       ).count()
        if (complaint_currentmonth and complaint_last_month)==0:
            percentage_difference_complaint='0%'
        if complaint_last_month > 0:
            if complaint_currentmonth >complaint_last_month:
                percentage_difference_complaint = f' +{((complaint_currentmonth - complaint_last_month) / complaint_last_month) * 100} %'
            else:
                percentage_difference_complaint= f' {((complaint_currentmonth - complaint_last_month) / complaint_last_month) * 100} %'
        
        else:
            percentage_difference_complaint ='100%'

        

        total_dealer_count=franchisee.dealers
        
        dealer_currentmonth = Dealer.objects.filter(
                           franchisee=franchisee,
                           created_date__gte=first_day_of_month,
                           created_date__lte=now
                           ).count()

        dealer_last_month = Dealer.objects.filter(
           created_date__range=[first_day_of_last_month, last_day_of_last_month],
           franchisee=franchisee
        ).count()
        if (dealer_currentmonth and dealer_last_month)==0:
            percentage_difference_dealer='0%'
        if dealer_last_month > 0:
            if dealer_currentmonth >dealer_last_month:
                percentage_difference_dealer = f' +{((dealer_currentmonth - dealer_last_month) / dealer_last_month) * 100} %'
            else:
                percentage_difference_dealer= f' {((dealer_currentmonth - dealer_last_month) / dealer_last_month) * 100} %'
        
        else:
            percentage_difference_dealer ='100%'

        
                 

        total_serviceprovider_count=franchisee.service_providers
        serviceprovider_currentmonth = ServiceProvider.objects.filter(
                           franchisee=franchisee,
                           created_date__gte=first_day_of_month,
                           created_date__lte=now
                           ).count()
        serviceprovider_last_month = ServiceProvider.objects.filter(
           created_date__range=[first_day_of_last_month, last_day_of_last_month],
           franchisee=franchisee
        ).count()
        if (serviceprovider_currentmonth and serviceprovider_last_month)==0:
            percentage_difference_serviceprovider='0%'
        if serviceprovider_last_month > 0:
            if serviceprovider_currentmonth >serviceprovider_last_month:
                percentage_difference_serviceprovider = f' +{((serviceprovider_currentmonth - serviceprovider_last_month) / serviceprovider_last_month) * 100} %'
            else:
                percentage_difference_serviceprovider= f' {((serviceprovider_currentmonth - serviceprovider_last_month) / serviceprovider_last_month) * 100} %'
        
        else:
            percentage_difference_serviceprovider ='100%'


        
        
            
        
        return Response({"total_services": service_count,
                         "service lastmonth":percentage_difference_service,
                         "total number of service providers":franchisee.service_providers,
                         "service provider last month":percentage_difference_serviceprovider,
                         "total number of dealers":franchisee.dealers,
                         "dealer last month":percentage_difference_dealer,
                         "total number of ads":total_ads_count,
                         "ad last month":percentage_difference_ad,
                         "total number of complaints":total_complaints_count,
                         "complaint last month":percentage_difference_complaint
                         }, 
                         status=status.HTTP_200_OK)
        
        