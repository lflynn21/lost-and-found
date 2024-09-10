from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from home.forms import FoundItemForm, LostItemForm
from home.views import lost_item_form
from home.models import Hub, LostItem, Location, FoundItem
from django.contrib.auth.models import User

class LostItemFoundItemDetailViewTest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username="testuser", password="testpass", email= "testemail@gmail.com")
        self.location = Location.objects.create(latitude=38.0359, longitude=-78.5037)
        self.client.login(username="testuser", password="testpass")
        # Create some test lost items
        # self.item1 = LostItem.objects.create(username=self.user, category="Water Bottle", description="blue plastic bottle", reward=5.0)
        # self.item2 = LostItem.objects.create(username=self.user, category="Keys", description="car keys with a red keychain", reward=10.0)


    def test_post_valid_lost_item_form(self):
        # Check that the new lost item is saved in the database
        new_item = LostItem.objects.create(user=self.user, location=self.location, category="Friend", description="my best friend Bob", reward=100.0)
        #check if it is the item
        self.assertEqual(new_item.user, self.user)
        self.assertEqual(new_item.location, self.location)
        self.assertEqual(new_item.description, "my best friend Bob")
        self.assertEqual(new_item.reward, 100.0)

    def test_delete_found_item(self): #this is the remove posting button for fonud item
        new_item = FoundItem.objects.create(user=self.user, location=self.location, category="Keys", item_description="Silver")
        # Send a POST request with 'delete' to the view
        response = self.client.post(reverse('home:found-detail', args=[new_item.id]), data={'delete': 'Remove Posting'})
        # Check if the response redirects to the index page
        self.assertRedirects(response, reverse('home:index'))
        # Check if the found item is deleted from the database
        self.assertFalse(FoundItem.objects.filter(id=new_item.id).exists())

    '''
    need selenium I think to test the thing since it is not a form cannot use post. I am not going to use selenium hehe

    def test_this_is_mine_button(self): #this tests the this is mine button for found item
        new_item = FoundItem.objects.create(user=self.user, location=self.location, category="Keys", item_description="Silver")
        # Check that the this is mine button creates a new found item in the database
        response = self.client.post(reverse('home:found-detail', args=[new_item.id]), data={'delete': 'This is Mine!'})
        # Check if the response redirects to the found item detail page
        self.assertRedirects(response, reverse('home:claimed-item', args=[new_item.id]))
        # Check if the found item is created in the database
        self.assertTrue(FoundItem.objects.filter(id=new_item.id).exists())
    '''

    def test_delete_your_lost_item(self): #this is remove posting for lost item
        new_item = LostItem.objects.create(user=self.user, location=self.location, category="Friend", description="and his name is bababooey", reward = 2.0)
        # Send a POST request with 'delete' to the view
        response = self.client.post(reverse('home:lost-detail', args=[new_item.id]), data={'delete': 'Remove Posting'})
        # Check if the response redirects to the index page
        self.assertRedirects(response, reverse('home:index'))
        # Check if the found item is deleted from the database
        self.assertFalse(LostItem.objects.filter(id=new_item.id).exists())
    
    def test_delete_other_lost_item(self): #delete a lost item posting that is not yours
        # Other user
        #need to fill out email field as that is the criteria used to see if users are the same took me some time to realize why it wasn't passing >:(
        self.user2 = User.objects.create_user(username="testuser2", email = "goku@gmail.com", password="testpass2")
        

        new_item = LostItem.objects.create(user=self.user, location=self.location, category="Friend", description="and his name is bababooey", reward = 2.0)
        

        # Log in as a different user
        self.client.login(username="testuser2", password="testpass2")

        # Send a POST request with 'delete' to the view
        response = self.client.post(reverse('home:lost-detail', args=[new_item.id]), data={'delete': 'Remove Posting'})

        #pop up response
        self.assertContains(response, 'Only the user who reported they lost the item is allowed to delete this post!')

        # Check if the LostItem still exists in the database
        self.assertTrue(LostItem.objects.filter(id=new_item.id).exists())


class LostItemFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.location = Location.objects.create(latitude=38.0359, longitude=-78.5037)
        self.client.login(username="testuser", password="testpass")

    def test_submit_lost_item_form(self):
        form_data = {
            'category': 'Others',
            'description': 'the red sea',
            'reward': 10.0,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
        }

        form = LostItemForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Create a POST request to the view that handles the form submission
        response = self.client.post(reverse('home:report-lost'), data=form_data)

        # Check if the form submission redirects to home
        self.assertRedirects(response, reverse('home:index'))

        self.assertTrue(LostItem.objects.filter(category='Others', description='the red sea', reward=10.0).exists())

class FoundItemFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.location = Location.objects.create(latitude=38.0359, longitude=-78.5037)
        self.client.login(username="testuser", password="testpass")

        # Create a test hub
        self.hub = Hub.objects.create(location=self.location, name="My van", description="I have free candy hehe", approved=True)

    def test_submit_found_item_form(self):
        form_data = {
            'category': 'Keys',
            'item_description': 'Silver keys', 
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
            'hub': self.hub.id,
        }

        form = FoundItemForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Create a POST request to the view that handles the form submission
        response = self.client.post(reverse('home:report-found'), data=form_data)

        # Check if the form submission redirects to home
        self.assertRedirects(response, reverse('home:index'))

        self.assertTrue(FoundItem.objects.filter(category='Keys', item_description='Silver keys').exists())

class HubRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_request_hub_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('home:request-hub'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'name': 'My home',
            'description': 'hehe',
            'latitude': '77.77', 
            'longitude': '77.77'
        }
        response = self.client.post(reverse('home:request-hub'), data=form_data)

        self.assertRedirects(response, reverse('home:index'))

        # Check if the hub object was created and not approved yet
        self.assertTrue(Hub.objects.filter(name='My home', approved=False).exists())

class ApproveHubTest(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)

        self.location = Location.objects.create(latitude=38.0359, longitude=-78.5037)

        # Create a hub to be approved
        self.hub = Hub.objects.create(name='Hub to Approve', description='Hub Description', location = self.location)

    def test_approve_hub_view(self):
        # Login as the admin user
        self.client.login(username='adminuser', password='adminpassword')

        response = self.client.get(reverse('home:approve-hubs'))
        self.assertEqual(response.status_code, 200)

        # Perform the hub approval
        response = self.client.get(reverse('home:approve-hub', kwargs={'hub': self.hub.id}))

        self.assertRedirects(response, reverse('home:index'))

        # Check if the hub object is now approved
        self.hub.refresh_from_db()
        self.assertTrue(self.hub.approved)