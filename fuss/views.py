from django.shortcuts import render
from django.http import HttpResponseRedirect
import forms
import models

def player_registration(request):
    if request.method == 'POST':
        form = forms.PlayerRegistrationForm(request.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            full_name = form.cleaned_data['full_name']
            e_mail = form.cleaned_data['e_mail']
            e_mail_me = form.cleaned_data['e_mail_me']
            new_player = models.Player(
                    nick=nick,
                    full_name=full_name,
                    e_mail=e_mail,
                    e_mail_me=e_mail_me
                )
            new_player.save()
            # mailing_list.append(e_mail)
            return HttpResponseRedirect('/fuss/thanks/')
    else:
        form = forms.PlayerRegistrationForm()

    return render(request, 'player_registration', {
            'form': form,
            })

def thanks(request):
    return render(request, 'thanks')
