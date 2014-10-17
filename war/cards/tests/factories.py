# from cards import
import factory
from cards.models import Player, WarGame


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'
    result = WarGame.TIE

class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player
    username = factory.Sequence(lambda i: 'User%d' % i)
    # email = factory.Sequence(lambda i: 'test%d@test.com' % i)
    email = factory.lazy_attribute(lambda o: '%s@gmail.com' % o.username)
    password = factory.PostGenerationMethodCall("set_password", "password") #this will then hash the password instead of directly dropping into db


    # email = factory.lazy_attribute_sequence(lambda o, n: '%s%d@gmail.com' % o.username, i)
    # profile = factory.SubFactory(ProfileFactory)
    # @factory.Sequence -> more verbose version of lambda
    # def username(counter):
    #     return "user%d" % counter

# p = PlayerFactory(profile__name="johnson")
