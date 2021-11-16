from django.db import models

# Create your models here.

from billing.models import BillingProfile


ADDRESS_TYPES = (
            # ('billing', 'Facturacion'), # ('billing','Billing'),
            ('shipping', 'Envio'), # ('shipping','Shipping'),
                )

class Address(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type            = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    direccion_linea_1       = models.CharField(max_length=120)
    direccion_linea_2       = models.CharField(max_length=120, null=True, blank=True)
    # pais                    = models.CharField(max_length=120, default='Costa Rica')
    provincia               = models.CharField(max_length=120)
    canton                  = models.CharField(max_length=120)
    distrito                = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)


    def get_address(self):
        return "{linea1} {linea2}, {provincia}, {canton}, {distrito} ".format(   # {postal}
                linea1      = self.direccion_linea_1,
                linea2      = self.direccion_linea_2 or "",
                # pais        = self.pais,
                provincia   = self.provincia,
                canton      = self.canton,
                distrito    = self.distrito,
        )
