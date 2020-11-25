# from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
# from flask_login import current_user, login_required
# from flaskblog import db
# from flaskblog.models import Post
# from flaskblog.posts.forms import PostForm

# posts = Blueprint('posts', __name__)

# @posts.route('/posts')
# def allPosts():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(
#         Post.datePosted.desc()).paginate(page=page, per_page=5)
#     return render_template('posts.html', posts=posts, title='Posts')


# @posts.route('/post/<int:postId>')
# def post(postId):
#     post = Post.query.get_or_404(postId)
#     return render_template('post.html', title=post.title, post=post)


# @posts.route('/post/new', methods=['GET', 'POST'])
# @login_required
# def newPost():
#     form = PostForm()
#     if form.validate_on_submit():
#         newPost = Post(title=form.title.data,
#                        content=form.content.data, author=current_user)
#         db.session.add(newPost)
#         db.session.commit()
#         flash('Post created', 'success')
#         return redirect(url_for('posts.allPosts'))
#     return render_template('newPost.html', title='New Post', form=form, legend='New Post')


# @posts.route('/post/<int:postId>/edit', methods=['GET', 'POST'])
# @login_required
# def edit(postId):
#     post = Post.query.get_or_404(postId)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Post has been updated', 'success')
#         return redirect(url_for('posts.allPosts', postId=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('editPost.html', title="Edit Post", form=form, legend='Edit Post')


# @posts.route('/deletePost/<int:postId>', methods=['POST'])
# @login_required
# def deletePost(postId):
#     post = Post.query.get_or_404(postId)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Post has been deleted', 'success')
#     return redirect(url_for('posts.allPosts'))