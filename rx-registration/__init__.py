
from django.conf import settings

import stripe


def get_stripe():
    stripe.api_key = settings.STRIPE_API_SECRET_KEY
    return stripe
