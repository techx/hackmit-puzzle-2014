from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from catgif.models import Post, Comment
from flask.ext.mongoengine.wtf import model_form
from flask.ext.stormpath import login_required
import random

posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):
    decorators = [login_required]

    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):
    decorators = [login_required]

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)

class RegisterEndpoint(MethodView):
    def post(self, slug):
        posts = Post.objects.find({'slug':slug})
        print str(posts) + ' hi'
        if len(posts) > 0:
            rand_str = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
            calc_str = ''
            for i in range(0,7):
                calc_str += rand_str[random.randint(0,61)]
            old_code = OldCode()
            old_code.slug = posts[0].slug
            posts.slug = calc_str
            old_code.save()


# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/register/<slug>/', view_func=RegisterEndpoint.as_view('register'))