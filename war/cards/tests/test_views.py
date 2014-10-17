from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from mock import patch, Mock
from cards.models import WarGame, Player
from cards.tests.factories import WarGameFactory, PlayerFactory
from cards.utils import create_deck


class ViewTestCase(TestCase):
    def setUp(self):
        create_deck()

    @patch('cards.utils.requests')
    def test_home_page(self, mock_requests):
        mock_comic = {
            'num': 1433,
            'year': "2014",
            'safe_title': "Lightsaber",
            'alt': "A long time in the future, in a galaxy far, far, away.",
            'transcript': "An unusual gamma-ray burst originating from somewhere far across the universe.",
            'img': "http://imgs.xkcd.com/comics/lightsaber.png",
            'title': "Lightsaber",
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_requests.get.return_value = mock_response

        response = self.client.get(reverse('home'))
        self.assertIn('<h3>{} - {}</h3>'.format(mock_comic['safe_title'], mock_comic['year']), response.content)
        self.assertIn('<img alt="{}" src="{}">'.format(mock_comic['alt'], mock_comic['img']), response.content)
        self.assertIn('<p>{}</p>'.format(mock_comic['transcript']), response.content)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertInHTML('<p>Q: Can I win real money on this website?</p>', response.content)

    def test_filters_page(self):
        response = self.client.get(reverse('filters'))
        self.assertIn('Uppercased Rank: ACE', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_login_page(self):
        # password = 'passsword'
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        user = PlayerFactory.create_batch(1)[0]

        data = {
            'username': user.username,
            'password': user.password
        }
        self.client.post(reverse('login'), data)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'phone': '650-111-2222',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        # print "this is my player {}".format(Player.objects.filter(username=username))
        self.assertTrue(Player.objects.filter(username=username).exists())

        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

        # Set up some war game entries using WarGameFactory
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)


        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertInHTML('<p>Your game record is {}</p>'.format(user.get_record_display()), response.content)

        self.assertEqual(len(response.context['games']), 5)
        self.assertEqual(response.context['wins'], 2)
        self.assertEqual(response.context['losses'], 3)

    # def test_leaderboard_page(self):
    #     #Get the leaderboard Page
    #     response = self.client.get(reverse('leaderboard'))
    #
    #
    #
    #     # Create users with PlayerFactory
    #     user1 = PlayerFactory.create_batch(1)
    #     user2 = PlayerFactory.create_batch(1)
    #
    #     # Set up some war game entries using WarGameFactory
    #     WarGameFactory.create_batch(3, player=user1, result=WarGame.LOSS)
    #     WarGameFactory.create_batch(3, player=user1, result=WarGame.WIN)
    #     WarGameFactory.create_batch(1, player=user2, result=WarGame.WIN)
    #     WarGameFactory.create_batch(1, player=user2)
    #
    #     #Test the leaderboard
    #     self.assertEqual(len(response.context['leaderboard_score']), 4)


