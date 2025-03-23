from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import razorpay
import os

# Initialize Razorpay client with environment variables
client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

@csrf_exempt
@require_http_methods(["POST"])  # Ensure that only POST requests are handled
def initiate_payment(request):
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        amount = data.get('amount')
        currency = data.get('currency', 'INR')  # Default currency to 'INR' if not provided

        # Convert amount to paise by multiplying by 100 (if the amount is given in rupees)
        amount_paise = int(float(amount) * 100)

        # Create order with Razorpay client
        payment_data = {
            "amount": amount_paise,
            "currency": currency,
            "payment_capture": '1'
        }
        payment = client.order.create(data=payment_data)
        print("Payment Data:", payment)  # Log output to console

        return JsonResponse(payment, status=200)  # Return the payment data as JSON response
    except Exception as e:
        print("Error processing payment:", str(e))  # Log the error
        return JsonResponse({'error': 'Failed to process payment'}, status=500)
