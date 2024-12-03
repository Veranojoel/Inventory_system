from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Product, Category
from .models import SalesTerminal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .forms import SalesTerminalForm
import json

# Sales_terminal View
def sales_terminal(request):
    products_in_terminal = request.session.get("sales_terminal", [])
    categories = Category.objects.all()
    selected_category = request.GET.get("category")

    if selected_category:
        products = Product.objects.filter(category_id=selected_category)
    else:
        products = Product.objects.all()

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "products": products,
        "sales_products": products_in_terminal,
    }
    return render(request, "sales_terminal.html", context)

#Logic for product selection
@csrf_protect
def add_to_sales_terminal(request):
    if request.method == "POST":
        # Extract product data from the form
        product = {
            "name": request.POST.get("product_name"),
            "barcode": request.POST.get("barcode"),
            "description": request.POST.get("description"),
            "price": request.POST.get("price"),
        }
        
        # Initialize session list for sales terminal if not exists
        if "sales_terminal" not in request.session:
            request.session["sales_terminal"] = []

        # Add selected product to the session
        request.session["sales_terminal"].append(product)
        request.session.modified = True  # Mark session as modified
        
        return redirect("sales_terminal")  # Redirect back to the sales terminal view
    return redirect("sales_terminal")

# CLear Btn
def clear_sales_terminal(request):
    # Remove sales terminal data from the session
    if "sales_terminal" in request.session:
        del request.session["sales_terminal"]
    return redirect("sales_terminal")  # Redirect back to the sales terminal page
