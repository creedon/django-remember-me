from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache

from remember_me.forms import AuthenticationRememberMeForm


def remember_me_login (
    request,
    template_name = 'registration/login.html',
    redirect_field_name = REDIRECT_FIELD_NAME,
    form_class = AuthenticationRememberMeForm,
    ):

    """
    Based on login view cribbed from
    django/trunk/django/contrib/auth/views.py
    
    Displays the login form with a remember me checkbox and handles the
    login action.
    
    In addition to the standard parameters of Django's login view
    function there is a form_class parameter.  By default,
    ``remember_me.forms.AuthenticationRememberMeForm`` will be used as
    the login form; to change this, pass a different form class as the
    ``form_class`` parameter.
    
    """
    
    from django.conf import settings
    from django.contrib.sites.models import RequestSite, Site
    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    
    redirect_to = request.REQUEST.get ( redirect_field_name, '' )
    
    if request.method == "POST":
    
        form = form_class ( data = request.POST, )
        
        if form.is_valid ( ):
        
            # Light security check -- make sure redirect_to isn't garbage.
            
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            if not form.cleaned_data [ 'remember_me' ]:
            
                request.session.set_expiry ( 0 )
                
            from django.contrib.auth import login
            
            login ( request, form.get_user ( ) )
            
            if request.session.test_cookie_worked ( ):
            
                request.session.delete_test_cookie ( )
                
            return HttpResponseRedirect ( redirect_to )
            
    else:
    
        form = form_class ( request, )
        
    request.session.set_test_cookie ( )
    
    if Site._meta.installed:
    
        current_site = Site.objects.get_current ( )
        
    else:
    
        current_site = RequestSite ( request )
        
    return render_to_response (
            template_name,
            {
                'form': form,
                redirect_field_name: redirect_to,
                'site': current_site,
                'site_name': current_site.name,
                },
            context_instance = RequestContext ( request ),
            )
remember_me_login = never_cache ( remember_me_login )
