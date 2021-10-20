# from pyramid.authentication import AuthTktAuthenticationPolicy
# from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config

# from .forms import TaskForm
from .security import SecurityPolicy

from .models import DBSession, Base

def main(global_config, **settings):
    # authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    # authorization_policy = ACLAuthorizationPolicy()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    config = Configurator(settings=settings,
                          root_factory='tutorial.models.Root',
                          session_factory=my_session_factory)
    config.include('pyramid_chameleon')

    config.set_security_policy(
        SecurityPolicy(
            secret=settings['tutorial.secret'],
        ),
    )

    config.add_route('home', '/')
    config.add_route('sanpham', '/howdy')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # config.add_route('wikipage_add', '/add')
    # config.add_route('wikipage_view', '/{id_sp}')
    # config.add_route('wikipage_edit', '/{uid}/edit')
    # config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()