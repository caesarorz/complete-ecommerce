from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

class MarketingPreference(models.Model):
    user                        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed                  = models.BooleanField(default=True)
    mailchimp_subscribed        = models.NullBooleanField(blank=True)
    mailchimp_msg               = models.TextField(null=True, blank=True)
    timestamp                   = models.DateTimeField(auto_now_add=True)
    updated                     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


#########################
def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    print("marketing_pref_create_receiver")
    print("instance", instance)
    if created:
        status_code, response_data = Mailchimp().subscribe(instance.user.email)
        # Mailchimp().add_email(instance.user.email)
        # response_data = Mailchimp().subscribe(instance.user.email)
        print("status_code", status_code, "response_data", response_data)

post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)


##################3
def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    print("marketing_pref_update_receiver")
    print("instance", instance)
    if instance.subscribed != instance.mailchimp_subscribed:
        # subscribing user
        if instance.subscribed:
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
            print("+++", status_code, " *** ", response_data)
        # unsubscribing user
        else:
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)
            print("+++", status_code, " *** ", response_data)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
            print("+++", status_code, " *** ", response_data)
        else:
            instance.subscribe = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data
            print("+++", status_code, " *** ", response_data)

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)


##############3
def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    print("make_marketing_pref_receiver")
    '''
    User model, when I create a user, I also create a marketing
    '''
    if created:
        print("make_marketing_pref_receiver instance", instance)
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)





'''
def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().subscribe(instance.user.email)
        print(status_code, response_data)


post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            # subscribing user
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
        else:
            # unsubscribing user
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)



def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    User model
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)
'''



#
#
# def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         status_code, response_data = Mailchimp().subscribe(instance.user.email)
#         print(status_code, response_data)
#
#
# post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)
#
# def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
#     if instance.subscribed != instance.mailchimp_subscribed:
#         if instance.subscribed:
#             # subscribing user
#             status_code, response_data = Mailchimp().subscribe(instance.user.email)
#         else:
#             # unsubscribing user
#             status_code, response_data = Mailchimp().unsubscribe(instance.user.email)
#
#         if response_data['status'] == 'subscribed':
#             instance.subscribed = True
#             instance.mailchimp_subscribed = True
#             instance.mailchimp_msg = response_data
#         else:
#             instance.subscribed = False
#             instance.mailchimp_subscribed = False
#             instance.mailchimp_msg = response_data
#
# pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)
#
#
#
#

# from django.conf import settings
# from django.db import models
# from django.db.models.signals import post_save, pre_save
#
# # Create your models here.
#
# from .utils import Mailchimp
#
# class MarketingPreference(models.Model):
#     user                    = models.OneToOneField(settings.AUTH_USER_MODEL)
#     subscribed              = models.BooleanField(default=True)
#     mailchimp_subscribed    = models.NullBooleanField(blank=True)
#     mailchimp_msg           = models.TextField(null=True, blank=True)
#     timestamp               = models.DateTimeField(auto_now_add=True)
#     update                  = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.email
#

    # if instance.subscribed != instance.mailchimp_subscribed:
    #     if instance.subscribed:
    #         # subscribe User
    #         status_code, response_data = Mailchimp().subscribe(instance.user.email)
    #     else:
    #         # unsubscribe user
    #         status_code, response_data = Mailchimp().unsubscribe(instance.user.email)
    #
    #     if response_data['status'] == 'subscribed':
    #         instance.subscribed = True
    #         instance.mailchimp_subscribed = True
    #         instance.mailchimp_msg = response_data
    #     else:
    #         instance.subscribed = False
    #         instance.mailchimp_subscribed = False
    #         instance.mailchimp_msg = response_data



# def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
#     """
#     user model
#     """
#     if created:
#         MarketingPreference.objects.get_or_create(user=instance)
#
# post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)
#

# def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print(status_code, " " ,response_data)
#         status_code, response_data = Mailchimp().subscribe(instance.user.email)
#
# post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)
