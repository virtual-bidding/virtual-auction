import json
from django.shortcuts import render
from auction.models import Participant, Payment
from payments.constants import PaymentStatus
from payments.models import Order
from virtual_auction.settings import client
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def order_payment(request,pid):
    pid =int(pid)
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/" + str(pid),
                "razorpay_key": 'rzp_test_SB0rBFhDAVWgV5',
                "order": order,
            },
        )
    return render(request, "payment.html")

@csrf_exempt
def callback(request,pid):
    pid =int(pid)
    def verify_signature(response_data):
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            total = Participant.objects.get(id=pid)
            if request.method=="POST":
                pay = Payment.objects.get(pay="paid")
                total.payment=pay
                total.save()
            return render(request, "callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})