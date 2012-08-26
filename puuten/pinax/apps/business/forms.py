from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from business.models import *

class BusinessProfileForm(forms.ModelForm):
    
    class Meta:
        model = BusinessProfile
        exclude = ('creator', 'created_at', 'status', 'picurl')
    

class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

    
class InviteManageForm(UserForm):
    local_business_id = forms.IntegerField(widget=forms.HiddenInput)
    to_user_id = forms.IntegerField(widget=forms.HiddenInput)
    to_user = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField(label=_("Message"), required=False, widget=forms.Textarea(attrs = {'cols': '20', 'rows': '5'}))
    
    def clean_to_user(self):
        to_userid = self.cleaned_data["to_user_id"]
        try:
            User.objects.get(pk=to_userid)
        except User.DoesNotExist:
            raise forms.ValidationError(u"Unknown user.")
            
        return self.cleaned_data["to_user"]
    
    def save(self):
        to_user = User.objects.get(pk=self.cleaned_data["to_user_id"])
        local_business = BusinessProfile.objects.get(pk = self.cleaned_data["local_business_id"])
        message = self.cleaned_data["message"]
        invitation = ManageshipInvitation(to_user=to_user, from_user=self.user, local_business=local_business, message=message, status="2")
        invitation.save()
        # if notification:
        #    notification.send([to_user], "management_invite", {"invitation": invitation})
        #    notification.send([local_business.creator], "management_invite_sent", {"invitation": invitation})
        local_business.creator.message_set.create(message="Manageship requested with %s" % to_user.username) # @@@ make link like notification
        return invitation

class AppForm(forms.ModelForm):
    
    class Meta:
        model = App

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(AppForm, self).__init__(*args, **kwargs)
