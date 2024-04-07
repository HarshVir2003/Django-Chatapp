from django import forms


class socketInfo(forms.Form):
    socket_name = forms.CharField(max_length=20)
    user_name = forms.CharField(max_length=20)
