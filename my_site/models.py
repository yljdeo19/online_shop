from django.db import models
from django.template.defaultfilters import slugify
class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Good(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='img')
    is_discount = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "img/%s-%s" % (slug, filename)


class Images(models.Model):
    post = models.ForeignKey(Good, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

class Comment(models.Model):
    good = models.ForeignKey(Good,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Комментарий от {self.name} к {self.good}'


class BackCall(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return self.name