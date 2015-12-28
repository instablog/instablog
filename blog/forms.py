from django import forms
from blog.models import Post
from blog.models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'photo', 'tags', 'origin_url')

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 4:
            raise forms.ValidationError("more than 4")
        return title

    def clean(self):
        title = self.cleaned_data.get('title', '')
        content = self.cleaned_data.get('content', '')
        if len(title) < 4 or len(content) < 4:
            raise forms.ValidationError("more than 4")
        return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
