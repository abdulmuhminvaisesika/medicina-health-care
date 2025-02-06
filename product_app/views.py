from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm  # Assuming you will create a ProductForm for adding new products
from django.contrib.auth.decorators import login_required


# View to display all products
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_app/products.html', {'products': products})

# View to add a new product
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')  # Redirect to the list of products after adding
    else:
        form = ProductForm()

    return render(request, 'product_app/add_product.html', {'form': form})



from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, permissions
from .permissions import IsOwner

class OwnerProductsCrudOperation(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete by updating the active status into falswe 
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.is_stock = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        