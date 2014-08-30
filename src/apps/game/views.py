from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from game.models import Renner, Team, Etappe
from game.forms import RennerForm

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

def home(request):
    teams = Team.objects.all()
    renners = {}
    for team in teams:
        renners[team] = Renner.objects.filter(team=team)

    return render_to_response('renners.html', {'renners': renners})

class RennerView(TemplateView):
    template_name = 'renners.html'

    def get_context_data(self, **kwargs):
        '''
        to get kwargs of url, e.g.:
        x = self.kwargs.get('naam', None)
        '''
        
        context = super(RennerView, self).get_context_data(**kwargs)
        context['renners'] = {}
        teams = Team.objects.all()
        
        for team in teams:
            context['renners'][team] = Renner.objects.filter(team=team)

        context['user'] = self.request.user
        
        return context

class RennerFormView(FormView):
    form_class = RennerForm
    success_url = "/home/"
    template_name = "renner_form.html"


    def form_valid(self, form):
        print(self.request.POST['naam'])
        team = Team.objects.get(pk=self.request.POST['team'])
        renner = Renner.objects.get_or_create(naam=self.request.POST['naam'], nummer=self.request.POST['nummer'], team=team)
        return super(RennerFormView, self).form_valid(form)
        
