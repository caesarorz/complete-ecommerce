from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect

from .mixins import CsrfExemptMixin
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = "cea969e952"

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = 'Sus preferencias de correo han sido actualizadas. Gracias!'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/login/?next=/settings/email/")
            # return HttpResponse("Not Allowed", status=400)
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Actualizar Preferencias de Correo'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


'''
POST METHOD
data[merges][LNAME]:
data[list_id]: cea969e952
data[merges][EMAIL]: mmm@mm.com
type: subscribe
data[merges][PHONE]:
data[id]: 6bd289d94e
data[web_id]: 217783493
data[ip_opt]: 190.171.102.73
data[merges][ADDRESS]:
data[email]: mmm@mm.com
data[email_type]: html
fired_at: 2018-07-03 13:14:57
data[merges][FNAME]:
'''

MAILCHIMP_EMAIL_LIST_ID = "cea969e952"  # place this in one location

class MailchimpWebhookView(CsrfExemptMixin, View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Thank you", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if srt(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None

            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data))
        return HttpResponse("Thank you", status=200)

#
# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if srt(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#
#         if sub_status == "subscribed":
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == "unsubscribed":
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                         subscribed=is_subbed,
#                         mailchimp_subscribed=mailchimp_subbed,
#                         mailchimp_msg=str(data))
#     return HttpResponse("Thank you", status=200)
#


#
#
#
# class MarketingPreferenceUpdateView(SuccessMessageMixin ,UpdateView):
#     form_class = MarketingPreferenceForm
#     template_name = 'base/forms.html'
#     success_url = '/settings/email/'
#     success_message = 'Your email preferences have been updated. Thank you.'
#
#     def dispatch(self, *args, **kwargs):
#         user = self.request.user
#         if not user.is_authenticated():
#             return redirect('/login/?next=/settings/email/')# HttpResponse('Not allowed', status=400)
#         return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
#         context['title'] = "Update Email Preferences"
#         return context
#
#     def get_object(self):
#         user = self.request.user
#         obj, created = MarketingPreference.objects.get_or_create(user=user)
#         return obj
#
# """
# http://requestbin.fullcontact.com
# POST /19yyqzt1
#
# data[list_id]: 354afd790e
# data[email]: hello@cesar.com
# data[merges][FNAME]:
# fired_at: 2018-03-26 23:02:54
# data[web_id]: 190431817
# data[merges][BIRTHDAY]:
# data[ip_opt]: 201.191.254.227
# data[merges][PHONE]:
# data[reason]: manual
# data[merges][EMAIL]: hello@cesar.com
# data[id]: 672e09ec21
# type: unsubscribe
# data[merges][LNAME]:
# data[merges][ADDRESS]:
# data[email_type]: html
# """
#
# class MailchimpWebhookView(CsrfExemptMixin, View):
#     # def get(self, request, *args, **kwargs):
#     #     return HttpResponse('Thank you', status=200)
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST
#         list_id = data.get('data[list_id]')
#         if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#             hook_type = data.get('type')
#             email = data.get('data[email]')
#             response_status, response = Mailchimp().check_subcription_status(email)
#             sub_status = response['status']
#             is_subbed = None
#             mailchimp_subbed = None
#             if sub_status == 'subscribed':
#                 is_subbed, mailchimp_subbed = (True, True)
#             elif sub_status == 'unsubscribed':
#                 is_subbed, mailchimp_subbed = (False, False)
#             if is_subbed is not None and mailchimp_subbed is not None:
#                 qs = MarketingPreference.objects.filter(user__email__iexact=email)
#                 if qs.exists():
#                     qs.update(
#                         subscribed=is_subbed,
#                         mailchimp_subscribed=mailchimp_subbed,
#                         mailchimp_msg=str(data)
#                     )
#         return HttpResponse('Thank you', status=200)


# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subcription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                     subscribed=is_subbed,
#                     mailchimp_subscribed=mailchimp_subbed,
#                     mailchimp_msg=str(data)
#                 )
#     return HttpResponse('Thank you', status=200)
