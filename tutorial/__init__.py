from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config

from .security import SecurityPolicy

from .models import DBSession, Base

def main(global_config, **settings):

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    config = Configurator(settings=settings,
                          root_factory='.resources.Root',
                          session_factory=my_session_factory)
    config.include('pyramid_chameleon')

    config.set_security_policy(
        SecurityPolicy(
            secret=settings['tutorial.secret'],
        ),
    )
    # Class Home
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')
    config.add_route('manageAcc', '/manageAcc')
    
    # Class Product 
    config.add_route('sanpham', '/sanpham')
    config.add_route('search', '/search')
    config.add_route('ban', 'ban')
    config.add_route('sofa', 'sofa')
    config.add_route('addsanpham', '/addsanpham')
    config.add_route('updatesp', '/updatesp/{id_sp}')

    # Class Category
    config.add_route('danhmuc', '/danhmuc')
    config.add_route('adddanhmuc', '/adddanhmuc')
    config.add_route('updatedm', '/updatedm/{id_dm}')

    # config.add_route('login', '/login')

    config.add_route('createreport', '/createreport')
    config.add_route('createBBHDBH', '/createBBHDBH')
    config.add_route('createBBHDNH', '/createBBHDNH')
    config.add_route('create-bill', '/bill')
    config.add_route('create-hdbh', '/hdbh/{id_hdbh}')
    config.add_route('create-hdnh', '/hdnh/{id_hdnh}')

    config.add_route('addProductToBill', '/addproducttobill')



    # config.add_route('register', '/register')
    # config.add_route('logout', '/logout')

    config.scan('.views')
    return config.make_wsgi_app()