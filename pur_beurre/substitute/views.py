from django.template import loader
from django.http import HttpResponse


def homepage(request):
    template = loader.get_template('substitute/index.html')
    return HttpResponse(template.render(request=request))