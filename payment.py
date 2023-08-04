from fastapi import FastAPI, HTTPException
import paypalrestsdk

app = FastAPI()

paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "AfFycMurVv0K2CO7V9GBm3QkHSa4RvKtBRA8K6-UouULo-2FQ09vBQFGgj0PM7Q9cdVVf1VmZ0ecvpYr",
    "client_secret": "EK02KdFBLXPITr01nc2avHuPfs7eCcMm2hhNTnmR0x2VQeEvY95ay9FNN_-ujQaHoQ9GhFgGHVDBvjej"
})

@app.post("/create_payment/")
def create_payment(amount: float):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [
            {
                "amount": {
                    "total": "{:.2f}".format(amount),
                    "currency": "USD"
                },
                "description": "Payment description"
            }
        ],
        "redirect_urls": {
            "return_url": "",
            "cancel_url": ""
        }
    })

    if payment.create():
        return payment.links[1].href  # Redirect user to PayPal for payment
    else:
        raise HTTPException(status_code=500, detail="Payment creation failed.")