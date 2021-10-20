import colander

from pyramid.httpexceptions import (
    HTTPFound,
)

from pyramid.security import (
    remember,
    forget,
)

from pyramid.view import (
    view_config,
    view_defaults
)

from .security import (
    USERS
    # check_password,
    # hash_password
)

from .models import DBSession, SanPham, NhanVien


# class WikiPage(colander.MappingSchema):
#     title = colander.SchemaNode(colander.String())
#     body = colander.SchemaNode(
#         colander.String(),
#         widget=deform.widget.RichTextWidget()
#     )

@view_defaults(renderer='home.pt')
class WikiViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid
    # @property
    # def wiki_form(self):
    #     schema = WikiPage()
    #     return deform.Form(schema, buttons=('submit',))

    # @property
    # def reqts(self):
    #     return self.wiki_form.get_widget_resources()

    @view_config(route_name='home')
    def home(self):
        return {'name': 'Quản lý cửa hàng nội thất'}

    @view_config(route_name='sanpham', renderer='sanpham.pt')
    def wiki_view(self):
        sanphams = DBSession.query(SanPham)

        # for sanpham in sanphams:
        #     print(sanpham.__dict__)
        return dict(sanphams=sanphams)

    @property
    def counter(self):
        session = self.request.session
        if 'counter' in session:
            session['counter'] += 1
        else:
            session['counter'] = 1

        return session['counter']


    

    @view_config(route_name='login', renderer='login.pt')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/howdy'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''

        def changeToDict():
            nhanviens = DBSession.query(NhanVien).all()
            nvs = []
            for nhanvien in nhanviens:
                tnv = nhanvien.__dict__
                nvs.append(tnv)
            obj = {}
            for x in nvs:
                obj[x['username']] = x['password']
            USERS.update(obj)
            return USERS
        
        changeToDict()

        # print(USERS)

        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            hashed_pw = USERS.get(login)
            if hashed_pw:
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                 headers=headers)
            message = 'Failed login'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)

    # @view_config(route_name='wikipage_add',
    #              renderer='wikipage_addedit.pt')
    # def wikipage_add(self):
    #     form = self.wiki_form.render()

    #     if 'submit' in self.request.params:
    #         controls = self.request.POST.items()
    #         try:
    #             appstruct = self.wiki_form.validate(controls)
    #         except deform.ValidationFailure as e:
    #             # Form is NOT valid
    #             return dict(form=e.render())

    #         # Add a new page to the database
    #         new_title = appstruct['title']
    #         new_body = appstruct['body']
    #         DBSession.add(Page(title=new_title, body=new_body))

    #         # Get the new ID and redirect
    #         page = DBSession.query(Page).filter_by(title=new_title).one()
    #         new_uid = page.uid

    #         url = self.request.route_url('wikipage_view', uid=new_uid)
    #         return HTTPFound(url)

    #     return dict(form=form)


    # @view_config(route_name='wikipage_view', renderer='wikipage_view.pt')
    # def wikipage_view(self):
    #     id_sp = int(self.request.matchdict['id_sp'])
    #     sanpham = DBSession.query(SanPham).filter_by(id_sp=id_sp).one()
    #     return dict(sanpham=sanpham)


    # @view_config(route_name='wikipage_edit',
    #              renderer='wikipage_addedit.pt')
    # def wikipage_edit(self):
    #     uid = int(self.request.matchdict['uid'])
    #     page = DBSession.query(Page).filter_by(uid=uid).one()

    #     wiki_form = self.wiki_form

    #     if 'submit' in self.request.params:
    #         controls = self.request.POST.items()
    #         try:
    #             appstruct = wiki_form.validate(controls)
    #         except deform.ValidationFailure as e:
    #             return dict(page=page, form=e.render())

    #         # Change the content and redirect to the view
    #         page.title = appstruct['title']
    #         page.body = appstruct['body']
    #         url = self.request.route_url('wikipage_view', uid=uid)
    #         return HTTPFound(url)

    #     form = self.wiki_form.render(dict(
    #         uid=page.uid, title=page.title, body=page.body)
    #     )

    #     return dict(page=page, form=form)
