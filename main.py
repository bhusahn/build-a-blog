from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:iyswtric17@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'abcdefghij'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_entry = request.form['blog-entry']
        new_blog = Blog(blog_title, blog_entry)
        db.session.add(new_blog)
        db.session.commit()
    
    blogs = Blog.query.all()

    return render_template('main-blog-page.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_new_blog():
    if request.method == 'POST':
        
        blog_title = request.form['blog-title']
        blog_entry = request.form['blog-entry']
        titleerror =''
        entryerror =''
        error = False
        
        if not blog_title or blog_title.strip() =='':
            titleerror = "Please provide a blog title."
            error=True
        if not blog_entry or blog_entry.strip() =='':
            entryerror = "Please provide a blog entry."
            error=True
        if error:
            return render_template('add-new-blog.html', entryerror=entryerror, titleerror=titleerror,
        blog_entry=blog_entry, blog_title=blog_title)
        else:
            new_blog = Blog(blog_title, blog_entry)
            db.session.add(new_blog)
            db.session.commit()
        
            blog_id = Blog.query.get('id')
            if blog_id is None is True:
                return redirect("/")
            else:
            
                blog=Blog.query.get('id')
                return render_template("new-blog-submission.html", blog_title=blog_title, blog_entry=blog_entry)

           
    return render_template('add-new-blog.html')
@app.route('/blog', methods=['POST','GET'])
def new_blog():
    if request.method == 'POST':
        blog_id = int(request.form['blog-id'])
        blog_title = Blog.query.get(blog_id)
        blog_entry = Blog.query.get(blog_id)
        new_blog = Blog(blog_title, blog_entry)
        db.session.add(new_blog)
        db.session.commit()

        return render_template('new-blog-submission.html', title='Post', new_blog=new_blog)
    
    if request.method == 'GET':
        blog_id = request.args.get('id')
        if blog_id is None:
            blogs = Blog.query.all()
            return redirect('/')
    
        else:
            blog=Blog.query.get(int(blog_id))
            return render_template('main-blog-page.html', title="individual_blog", blogs=[blog])

if __name__ == '__main__':
    app.run()