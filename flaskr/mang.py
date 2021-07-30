from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('mang', __name__)

@bp.route('/')

def index():
    
    
    db = get_db()
    cursor=db.cursor()
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN imp_user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cursor.fetchall()
    db.commit()
    return render_template('mang/index.html', posts=posts)

@bp.route('/', methods=('GET', 'POST'))
def searching():
    if request.method == 'POST':
        search = request.form['search']
        
        error = None
        

        if not search:
            error = 'search is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor=db.cursor()
            cursor.execute("select id from post where title=(%s)",(search,))
            info=cursor.fetchone()
            if info is not None:
                cursor.execute("select p.id,p.title,p.body,p.created,p.author_id,u.username from post p,imp_user u where p.id=%s",(info[0],))
                posts=cursor.fetchall()
                return render_template('mang/search.html',posts=posts)
            else:
                
                return redirect(url_for('mang.index'))
            
    
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
      
        title = request.form['title']
        body = request.form['body']
        error = None
        

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor=db.cursor()
            cursor.execute(
                'INSERT INTO post (title, body,author_id)'
                'VALUES (%s, %s,%s)',
                (title, body,g.user[0])
            )
           
            
            db.commit()
            return redirect(url_for('mang.index'))

    return render_template('mang/create.html')

@bp.route('/<pid>/hashtag', methods=('GET', 'POST'))
@login_required
def hashtag(pid):
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        
        error = None
        

        if not hashtag:
            error = 'Hashtag is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor=db.cursor()
            cursor.execute(
                'INSERT INTO tag (name)'
                'VALUES (%s)',
                (hashtag,)
            )
            cursor.execute("SELECT * FROM tag order by id desc")
            info=cursor.fetchone()
            
            cursor.execute("SELECT id FROM post where id=(%s)",(pid,))
            info1=cursor.fetchone()
            cursor.execute("INSERT INTO tags_post(notes,tag) VALUES (%s,%s)",(info1[0],info[0]))
            db.commit()
            return redirect(url_for('mang.index'))

    return render_template('mang/hashtag.html')

@bp.route("/<pid>")
def details(pid):
    db =get_db()
    cursor = db.cursor()
    cursor.execute("SELECT p.title,p.body,p.created,p.author_id,u.id,u.username FROM post p,imp_user u WHERE p.author_id=u.id and p.id=%s",(pid,))
    info=cursor.fetchone()
    cursor.execute("select t.name from tags_post tp, tag t where tp.notes = (%s) and tp.tag = t.id", (pid,))
    tags = (x[0] for x in cursor.fetchall())
    title,body,created,author_id,user_id,username=info
    return render_template("mang/details.html",id=pid,title=title,body=body,created=created,author_id=author_id,user_id=user_id,username=username,tags=tags)
    
@bp.route("/search/<field>/<value>")
def search(field, value):
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select id from tag where name=%s",(value,))
    tag_id=cursor.fetchone()[0]
    
    
    cursor.execute(f"SELECT p.id, p.title, p.body, p.created, p.author_id, s.username from post p, imp_user s,tags_post t where (p.author_id = s.id and t.tag={tag_id}) and t.notes=p.id")
    
    posts= cursor.fetchall()
    return render_template('mang/index.html', posts = posts,tag=value)
    
    
    
@bp.route("/<pid>/edit", methods=["GET", "POST"])
def edit(pid):
    db = get_db()
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute("select p.title, p.created,p.body, s.username from post p, imp_user s where p.author_id = s.id and p.id = %s", (pid,))
        info = cursor.fetchone()
        cursor.execute("select t.name from tags_post tp, tag t where tp.notes = %s and tp.tag = t.id", (pid,))
        tags = (x[0] for x in cursor.fetchall())
        title, created, body, username = info
        
        return render_template("mang/edit.html",id = pid,title = title,created = created,body = body,username = username,tags = tags)
       
    elif request.method == "POST":
        title=request.form.get('title')
        description = request.form.get('description')
        
        cursor.execute("Update post SET body=(%s) WHERE id=%s",(description,pid))
        cursor.execute("Update post SET title=(%s) WHERE id=%s",(title,pid))
        
        db.commit()
        return redirect(url_for("mang.details", pid=pid), 302)
        
        
@bp.route("/<pid>/add_hashtag")
def add_hashtag(pid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT t.id,t.name FROM tag t,post p where p.id=%s ORDER BY t.id asc",(pid,));
    info=cursor.fetchall()
    
    return render_template("mang/addtag.html",infos=info,id=pid)

