from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Hola Twitter', max_length=100)
    image = models.ImageField(default='default.png')


    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    #Query para obtener un usuario y obtener todos los registros en comun para saber los que sigue
    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
                                        .values_list('to_user_id',flat=True)
        return User.objects.filter(id__in=user_ids)
    
    #Query para obtener un usuario y obtener todos los registros en comun para saber los seguidores
    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
                                        .values_list('from_user_id',flat=True)
        return User.objects.filter(id__in=user_ids)

class Post(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='posts')
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return self.content
    
class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
    
def create_user_profile(sender, instance , created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance , **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)