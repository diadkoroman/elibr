# -*- coding: utf-8 -*-
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from sqlalchemy import or_
from core.dbconn import sess
from models.library import Book, Author
from models.users import Elibr_User
from forms.auth import RegForm, AutForm
from forms.search import SearchForm
from forms.admin_options import AddEntryForm, UpdateEntryForm
from utils.csrftokens import gen_csrf_token
from utils.crypt.crypters import encrypt_sha224 as enc224

app = Flask(__name__)
app.debug = True
app.config.from_object('configs.main')



@app.before_request
def set_csrf():
    app.jinja_env.globals['csrf_token'] = gen_csrf_token




@app.route('/',methods=['GET','POST'])
def indexview():
    title = app.config.get('PAGETITLE') if app.config.get('PAGETITLE') else ''
    uname = session.get('uname') if session.get('uname') else None
    #####################################
    try:
        books = [(item.id,item.nazva,','.join([autor.imja for autor in item.authors])) for item in sess.query(Book).all()]
    except:
        books = None

    ############ РОБОТА ФОРМИ ПОШУКУ ##################
    if request.method == 'POST':
        sf = SearchForm(request.form)
        if sf.validate():
            try:
                searchbooks = sess.query(Book).filter(or_(Book.nazva == sf.searchf.data,
                Book.nazva.startswith(sf.searchf.data),
                Book.nazva.contains(sf.searchf.data),
                Book.nazva.endswith(sf.searchf.data)
                ))
                books = [(item.id,item.nazva,','.join([autor.imja for autor in item.authors])) for item in searchbooks]
                
                searchauthors = sess.query(Author).filter(or_(Author.imja == sf.searchf.data,
                Author.imja.startswith(sf.searchf.data),
                Author.imja.contains(sf.searchf.data),
                Author.imja.endswith(sf.searchf.data)
                ))
                books2=[]
                for item in searchauthors:
                    for b in item.books:
                        books2.append((b.id,b.nazva,','.join([autor.imja for autor in b.authors])))

                #search_byauthors = sess.query(Book).filter(Book.authors.id.in_(aut_ids))
                #books2 = [(item.id,item.nazva,','.join([autor.imja for autor in item.authors])) for item in search_byauthors]
                books = books + books2
            except:
                books=None
    else:
        pass
    ###################################################

    
    # якщо користувач не авторизований - він бачить дефолтну першу сторінку
    # авторизований користувач входить на першу для авторизованих
    if not session.get('user_auth_key'):
        return render_template('components/page.html',title=title,books=books)
    else:
        return render_template('components/page_aut.html',title=title,uname=uname,books=books)



@app.route('/login/',methods=['GET','POST'])
def loginview():
    title = app.config.get('PAGETITLE') if app.config.get('PAGETITLE') else ''
    uname=None
    af = AutForm(request.form)
    ########### РОБОТА ФОРМИ АВТОРИЗАЦІЇ ##############
    if request.method == 'POST':
        tkn = session.pop('_csrf_sess',None)
        #af = AutForm(request.form)
        if af.validate() and (tkn and request.form.get('_csrf_token') == tkn):
            ##
            try:
                registered = sess.query(Elibr_User).\
                filter(Elibr_User.nickname == af.u_login.data,Elibr_User.password ==enc224(af.u_passw.data)).count()
                # авторизація пройдена, якщо запис користувача є в БД
                if int(registered) == 1:
                    session['user_auth_key'] = enc224('{0}__{1}'.format(af.u_login.data,af.u_passw.data))
                    session['uname'] = uname =af.u_login.data
                    return redirect(url_for('indexview'))
                else:
                    flash('Такого користувача немає!'.decode('UTF-8'))
                    return render_template('components/autf.html',title = title,af=af)
            except:
                return render_template('components/autf.html',title = title,af=af)
        else:
            return render_template('components/autf.html',title = title,af=af)
    #####################################################
    return render_template('components/autf.html',title = title,af=af)




@app.route('/logout/',methods=['GET','POST'])
def logoutview():
    if session.get('user_auth_key'):
        session.pop('user_auth_key',None)
    if session.get('uname'):
        session.pop('uname',None)
    return redirect(url_for('indexview'))




@app.route('/admin/')
def adminview():
    if session.get('user_auth_key'):
        try:
            title = app.config.get('PAGETITLE') if app.config.get('PAGETITLE') else ''
            uname = session.get('uname') if session.get('uname') else None
            #
            addf = AddEntryForm(request.form)
            addf.authors_list.choices = [(str(item.id),item.imja) for item in sess.query(Author).all()]
            addf.books_list.choices = [(str(item.id),item.nazva) for item in sess.query(Book).all()]
            #
            #
            editf = UpdateEntryForm(request.form)
            editf.authors_list.choices = [(str(item.id),item.imja) for item in sess.query(Author).all()]
            editf.books_list.choices = [(str(item.id),item.nazva) for item in sess.query(Book).all()]
            #
            ############################################################
            books = [(item.id,item.nazva,','.join([autor.imja for autor in item.authors])) for item in sess.query(Book).all()]
            authors = [(item.id,item.imja) for item in sess.query(Author).all()]
            return render_template('components/adm_workspace.html',
            title=title,
            uname=uname,
            addf=addf,
            editf=editf,
            books=books,
            authors=authors)
        except:
            abort(404)
    else:
        abort(404)



@app.route('/admin/<option>/',methods=['GET','POST'])
def optionsview(option=None):
    options =('add','delete','update')
    if option is None:
        return redirect(url_for('adminview'))
    else:
        if session.get('user_auth_key'):
            #
            addf = AddEntryForm(request.form)
            addf.authors_list.choices = [(str(item.id),item.imja) for item in sess.query(Author).all()]
            addf.books_list.choices = [(str(item.id),item.nazva) for item in sess.query(Book).all()]
            #
            if request.method == 'POST':
                if option in options:
                    if option == 'add':
                        if addf.validate():
                            if addf.addtype.data == 'books':
                                book = Book()
                                book.nazva = addf.add.data
                                if isinstance(addf.authors_list.data,(list,tuple)):
                                    a_ids=[int(item) for item in addf.authors_list.data]
                                    book.authors=list(sess.query(Author).filter(Author.id.in_(a_ids)))
                                sess.add(book)
                                sess.commit()
                            
                            elif addf.addtype.data == 'authors':
                                author = Author()
                                author.imja = addf.add.data
                                if isinstance(addf.books_list.data,(list,tuple)):
                                    b_ids=[int(item) for item in addf.books_list.data]
                                    author.books=list(sess.query(Book).filter(Book.id.in_(b_ids)))
                                sess.add(author)
                                sess.commit()
                        return redirect(url_for('adminview'))
                        
                            
            if option == 'delete':
                if request.args.get('a'):
                    try:
                        aut = int(request.args.get('a'))
                        sess.query(Author).filter_by(id=aut).delete()
                        sess.commit()
                    except:
                        pass
                        
                elif request.args.get('b'):
                    try:
                        buk = int(request.args.get('b'))
                        sess.query(Book).filter_by(id=buk).delete()
                        sess.commit()
                    except:
                        pass
                return redirect(url_for('adminview'))

        else:
            return redirect(url_for('indexview'))




@app.route('/admin/update/',methods=['GET','POST'])
def updateview():
    if session.get('user_auth_key'):
        title = app.config.get('PAGETITLE') if app.config.get('PAGETITLE') else ''
        uname = session.get('uname') if session.get('uname') else None
        upd=None
        #
        editf = UpdateEntryForm(request.form)
        editf.authors_list.choices = [(str(item.id),item.imja) for item in sess.query(Author).all()]
        editf.books_list.choices = [(str(item.id),item.nazva) for item in sess.query(Book).all()]
 
        ############# РОБОТА ФОРМИ ##################
        if request.method == 'POST':
            if editf.validate():
                if editf.edittype.data == 'books':
                    buk = sess.query(Book).get(editf.upd_id.data)
                    buk.nazva = editf.upd.data
                    a_ids=[int(item) for item in editf.authors_list.data]
                    buk.authors=list(sess.query(Author).filter(Author.id.in_(a_ids)))
                    sess.add(buk)
                    sess.commit()
                elif editf.edittype.data == 'authors':
                    pass
                return redirect(url_for('adminview'))
        ##############################################
        else:
            if request.args.get('a') or request.args.get('b'):
                if request.args.get('a'):
                    aut_id = int(request.args.get('a'))
                    aut_item = sess.query(Author).get(aut_id)
                    upd = (str(aut_item.id),aut_item.imja,'authors')
                elif request.args.get('b'):
                    buk_id = int(request.args.get('b'))
                    buk_item = sess.query(Book).get(buk_id)
                    upd = (str(buk_item.id),buk_item.nazva,'books')

                return render_template('components/editf.html',
                title=title,
                uname=uname,
                editf=editf,
                upd = upd
                )
            else:
                return redirect(url_for('adminview'))
    else:
        return redirect(url_for('indexview'))



@app.route('/register/',methods=['GET','POST'])
def registerview():
    title = app.config.get('PAGETITLE') if app.config.get('PAGETITLE') else ''
    uname=None
    rf = RegForm(request.form)
    #################################################
    if not session.get('user_auth_key'):
        if request.method == 'POST':
            tkn = session.pop('_csrf_sess',None)
            #rf = RegForm(request.form)
            if rf.validate() and (request.form.get('_csrf_token') == tkn):
                try:
                    # перевірка на дублікати
                    registered = sess.query(Elibr_User).\
                    filter(Elibr_User.nickname == rf.r_login.data,Elibr_User.password ==enc224(rf.r_passw.data)).count()
                    # якщо дублікатів немає - реєструємо нового користувача

                    nu_eu = Elibr_User()
                    nu_eu.nickname =rf.r_login.data
                    nu_eu.password=enc224(rf.r_passw.data)
                    sess.add(nu_eu)
                    sess.commit()
                    
                    session['user_auth_key'] = enc224('{0}__{1}'.format(nu_eu.nickname,nu_eu.password))
                    session['uname']=uname=nu_eu.nickname
                    return redirect(url_for('indexview'))
                except:
                    return render_template('components/regf.html',title=title,rf=rf)
            else:
                return render_template('components/regf.html',title=title,rf=rf)
        return render_template('components/regf.html',title=title,rf=rf)
    else:
        return redirect(url_for('indexview'))




@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

app.secret_key = 'poweirtweoituwporeitkjdghsldkfdkljgh2387421987349128374)(*&)(*&*&*(&(*)'
