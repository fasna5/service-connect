
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from adminapp.serializer import CustomerSerializer,UserSerializer,PaymentSummarySerializer,ServiceRequestSerializer,SubcategorySerializer
from rest_framework import status
from accounts.models import Customer,User,Payment,ServiceRequest,Subcategory,Category,Service_Type,Collar
#from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter



# Create your views here.
class PaymentPagination(PageNumberPagination):
        page_size = 4  # Number of items per page
        page_size_query_param = 'page_size'
        



class UserDetails(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        customer_id = request.data.get('custom_id')  # Get customer_id from the request body
        if not customer_id:
            return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.select_related('user').get(custom_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the customer details along with related user details
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class CompletedPaymentListView(APIView):
        authentication_classes=[JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def post(self, request, *args, **kwargs):
           customer_id = request.data.get('custom_id')  # Get customer_id from the request body
           if not customer_id:
             return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)
           try:
            customer = Customer.objects.get(custom_id=customer_id)
            user=customer.user
            print(user)
           except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)


           # Fetch payments with status 'completed'
           payments = Payment.objects.filter(payment_status='completed',sender = user )
        
           # Apply pagination
           paginator =PaymentPagination()
           paginated_payments = paginator.paginate_queryset(payments, request)

           if not paginated_payments:  # If there are no payments for this page
             return Response({'detail': 'No more pages available.'}, status=status.HTTP_404_NOT_FOUND)
        
           # Serialize the data
           serializer = PaymentSummarySerializer(paginated_payments, many=True)
        
           # Return paginated response
           return paginator.get_paginated_response(serializer.data)

class ServiceRequestPagination(PageNumberPagination):
    page_size = 4  # Adjust based on your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class ServiceRequestListView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('custom_id')  # Get customer_id from the request body
        if not customer_id:
             return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(custom_id=customer_id)
            user=customer.user
            print(user)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the ServiceRequest objects, ordered by the most recent request date first
        service_requests=ServiceRequest.objects.filter(customer=user).order_by('-request_date')
        

        # Pagination logic
        paginator = ServiceRequestPagination()
        paginated_requests = paginator.paginate_queryset(service_requests, request)
        
        # Serialize the data
        serializer = ServiceRequestSerializer(paginated_requests, many=True)
        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
    
class SubcategoryPagination(PageNumberPagination):
    page_size = 4  # Adjust based on your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class SubcategoryListView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
       category = request.data.get('category')  # Get category from the request body
       if not category:
             return Response({'error': 'category is required'}, status=status.HTTP_400_BAD_REQUEST)
       try:
            category_instance = Category.objects.get(title=category)  # Find the Category by name or another field
            subcategory = Subcategory.objects.filter(category=category_instance)
            
       except Subcategory.DoesNotExist:
             return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

        

         # Pagination logic
       paginator = SubcategoryPagination()
       paginated_requests = paginator.paginate_queryset(subcategory, request)
        
        # Serialize the data
       serializer = SubcategorySerializer(paginated_requests, many=True)
        
         # Return the paginated response
       return paginator.get_paginated_response(serializer.data)
    
    def put(self,request):
        category = request.data.get('category')  # Get category from the request body
        if not category:
             return Response({'error': 'category is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category_instance = Category.objects.get(title=category)  # Find the Category by name or another field
            subcategories = Subcategory.objects.filter(category=category_instance)
            
        except Category.DoesNotExist:
             return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        # Make sure there are subcategories to update
        if not subcategories:
            return Response({'error': 'No subcategories found for this category'}, status=status.HTTP_404_NOT_FOUND)

        # Now we process the update logic
        updated_subcategories = []
        for subcategory in subcategories:
            # Assuming you're updating fields like title or other attributes of the subcategory.
            # Extract the data for update from the request, e.g. 'title', 'description', etc.
            subcategory_data = request.data.get(str(subcategory.id))  # Assuming subcategory data is passed by id
            
            if subcategory_data:
                subcategory.id=subcategory_data.get('id',subcategory.id)
                subcategory.title = subcategory_data.get('title', subcategory.title)
                subcategory.image=subcategory_data.get('image',subcategory.image)
                subcategory.description = subcategory_data.get('description', subcategory.description)
                subcategory.status = subcategory_data.get('status', subcategory.status)
                # Fetch Category, Service_Type, and Collar instances based on their IDs
                if 'category' in subcategory_data:
                    subcategory.category = Category.objects.get(id=subcategory_data['category'])

                if 'service_type' in subcategory_data:
                    subcategory.service_type = Service_Type.objects.get(id=subcategory_data['service_type'])

                if 'collar' in subcategory_data:
                    subcategory.collar = Collar.objects.get(id=subcategory_data['collar'])


                subcategory.save()
                updated_subcategories.append(subcategory)

        if updated_subcategories:
            # You can serialize the updated subcategory data if needed
            serializer = SubcategorySerializer(updated_subcategories, many=True)
            return Response({'updated_subcategories': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No subcategories were updated'}, status=status.HTTP_400_BAD_REQUEST)

class SubcategorySearch(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubcategorySerializer
    pagination_class = SubcategoryPagination
    filter_backends = [SearchFilter]
    # Adjust the search fields to allow searching in both 'category__title' and 'title' of Subcategory
    #search_fields = ['category__title', 'title']  # Searching in category title and subcategory title
    search_fields = ['title'] 
    def list(self, request, *args, **kwargs):
        # Get category from request body (JSON format)
        category = request.data.get('category')

        # Validate that the category is provided
        if not category:
            return Response({'error': 'Category is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the Category by title
            category_instance = Category.objects.get(title=category)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter the subcategories based on the category
        queryset = Subcategory.objects.filter(category=category_instance)

        # Apply search if search parameters are provided in the request (from URL)
        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # If no subcategories are found
        if not queryset.exists():
            return Response({'error': 'No subcategories found for this category'}, status=status.HTTP_404_NOT_FOUND)

        # Apply pagination and return the results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not used, return all the results
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class SubcategorySortView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
    serializer_class = SubcategorySerializer
    pagination_class = SubcategoryPagination

    def list(self, request, *args, **kwargs):
        # Get category from request body (JSON format)
        category = request.data.get('category')

        # Validate that the category is provided
        if not category:
            return Response({'error': 'Category is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the Category by title
            category_instance = Category.objects.get(title=category)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter the subcategories based on the category and sort by ID
        queryset = Subcategory.objects.filter(category=category_instance).order_by('id')

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination, return all the subcategories sorted by ID
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)