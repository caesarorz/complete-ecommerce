import hashlib
import json
import re
import requests
from django.conf import settings


# MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
# MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
# MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

MAILCHIMP_API_KEY = "81f4bebbdfc00c3c2ce1bb4fa0ef4778-us12"
MAILCHIMP_DATA_CENTER = 'us12'
MAILCHIMP_EMAIL_LIST_ID = "cea969e952"


def check_email(email):
    print("check_email")
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email

def get_subscriber_hash(member_email):
    print("get_subscriber_hash")
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()



class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(
                    dc=MAILCHIMP_DATA_CENTER
                    )
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
                                    api_url = self.api_url,
                                    list_id=self.list_id
                        )


    def get_members_endpoint(self):
        return self.list_endpoint + "/members"
    #
    # def change_subscription_status(self, email, status='unsubscribed'):
    #     hashed_email = get_subscriber_hash(email)
    #     endpoint = self.get_members_endpoint() + "/" +  hashed_email
    #     data = {
    #         "status": self.check_valid_status(status)
    #     }
    #     print(endpoint)
    #     r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
    #     return r.status_code, r.json()

    def add_email(self, email):
        print("add_email")
        status = "subscribed"
        self.check_valid_status(status)
        print("check_valid_status ", self.check_valid_status(status))
        data = {
            "email_address": email,
            "status": status
        }
        endpoint = self.get_members_endpoint()
        # endpoint = self.get_members_endpoint()
        r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.json()
        # return self.change_subscription_status(email, status='subscribed')

    def change_subscription_status(self, email, status="unsubscribed"):
        # hashed_email = get_subscriber_hash(email)
        # endpoint = self.get_members_endpoint() + "/" +  hashed_email
        # /lists/{list_id}/members/{subscriber_hash}
        # https://us12.api.mailchimp.com/3.0/lists/cea969e952/members/4645615a7b9e639cd7753fdd78cbb715
        print("change_subscription_status")
        hashed_email = get_subscriber_hash(email)
        print("hashed_email", hashed_email)

        endpoint = self.get_members_endpoint() + "/" + hashed_email # endpoint = self.api_url
        data = {
            "email_address": email,
            "status": self.check_valid_status(status),
        }
        print("data", data)
        print("endpoint", endpoint)
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        print("r", r, "r.status_code", r.status_code, "r.json()", r.json())
        return r.status_code, r.json()


    def check_subscription_status(self, email):
        print("check_subscription_status")
        # hashed_email = get_subscriber_hash(email)
        # endpoint = self.get_members_endpoint() + "/" +  hashed_email
        # /lists/{list_id}/members/{subscriber_hash}
        # https://us12.api.mailchimp.com/3.0/lists/cea969e952/members/4645615a7b9e639cd7753fdd78cbb715

        hashed_email = get_subscriber_hash(email)
        print("hashed_email", hashed_email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email # endpoint = self.api_url
        print("endpoint", endpoint)
        r = requests.get(endpoint, auth=("", self.key))
        print("r", r, "r.status_code", r.status_code, "r.json()", r.json())
        return r.status_code, r.json()

    def check_valid_status(self, status):
        print("check_valid_status")
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending'] # subscribed unsubscribed cleaned pending
        if status not in choices:
            print("error", status)
            raise ValueError("Not a valid choice for email status")
        print("status", status)
        return status
    #

    # def unsubscribe(self, email):
    #     return self.change_subscription_status(email, status='unsubscribed')
    def unsubscribe(self, email):
        print("unsubscribe")
        return self.change_subscription_status(email, status='unsubscribed')

    def subscribe(self, email):
        print("subscribe")
        return self.change_subscription_status(email, status='subscribed')

    def pending(self, email):
        print("pending")
        return self.change_subscription_status(email, status='pending')

    #
    # def subscribe(self, email):
    #     return self.change_subscription_status(email, status='subscribed')
    #
    # def pending(self, email):
    #     return self.change_subscription_status(email, status='pending')



# import hashlib
# import json
# import re
# import requests
# from django.conf import settings
#
# MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY', None)
# MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER', None)
# MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)
#
#
# def check_email(email):
#     if not re.match(r".+@.+\..+", email):
#         raise ValueError('String passed is not a valid email address')
#     return email
#
# def get_subscriber_hash(member_email):
#     check_email(member_email)
#     member_email = member_email.lower().encode()
#     m = hashlib.md5(member_email)
#     return m.hexdigest()
#
#
# class Mailchimp(object):
#     def __init__(self):
#         super(Mailchimp, self).__init__()
#         self.key = MAILCHIMP_API_KEY
#         self.api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(
#                                                 dc=MAILCHIMP_DATA_CENTER
#                                                 )
#         self.list_id = MAILCHIMP_EMAIL_LIST_ID
#         self.list_endpoint = '{api_url}/lists/{list_id}'.format(
#                                                     api_url = self.api_url,
#                                                     list_id=self.list_id
#                                                                 )
#
#     def get_members_endpoint(self):
#         return self.list_endpoint + '/members/'
#
#     def change_subscription_status(self, email, status='unsubscribed'):
#         hashed_email = get_subscriber_hash(email)
#         endpoint = self.get_members_endpoint() + '/' + hashed_email
#         data = {
#             "status": self.check_valid_status(status)
#         }
#         r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
#         return r.status_code, r.json()
#
#     def check_subscription_status(self, email):
#         hashed_email = get_subscriber_hash(email)
#         print('hashed_email in check_subscription_status ',hashed_email)
#         endpoint = self.get_members_endpoint() + "/" + hashed_email
#         print('endpoint in check_subscription_status: ',endpoint)
#         r = requests.get(endpoint, auth=("", self.key))
#         return r.status_code, r.json()
#
#     def check_valid_status(self, status):
#         # subscribed unsubscribed cleaned pending
#         choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
#         if status not in choices:
#             raise ValueError("Not a valid choice for email status")
#         return status
#
#     def add_email(self, email):
#     #     status = "subscribed"
#     #     self.check_valid_status(status)
#     #     data = {
#     #         "email_address": email,
#     #         "status": status,
#     #     }
#     #     endpoint = self.get_members_endpoint()
#     #     r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
#     #     return r.json()
#         return self.change_subscription_status(email, status='subscribed')
#
#     def unsubscribe(self, email):
#         return self.change_subscription_status(email, status='unsubscribed')
#
#     def subscribe(self, email):
#         print(email)
#         return self.change_subscription_status(email, status='subscribed')
#
#     def pending(self, email):
#         return self.change_subscription_status(email, status='pending')
