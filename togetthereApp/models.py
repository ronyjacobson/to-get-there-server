from django.db import models
import datetime

# Change your models (in models.py).
# Run python manage.py makemigrations <App Name> to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.



class User(models.Model):
    facebook_id = models.CharField(max_length=30, blank = True)
    first_name = models.CharField(max_length=35, db_index=True)
    last_name = models.CharField(max_length=35, db_index=True, blank = True)
    email = models.EmailField(db_index=True, blank = True)
    birthday = models.DateField(blank = True)
    created = models.DateTimeField(auto_now_add=True)

    # bday =  datetime.datetime(year, month, day)
    # user = User(facebook_id = '', first_name= '', last_name= '', email = '', birthday=bday)

    def age(self):
        return (datetime.datetime.now().date() - self.birthday).days / 365

    def __unicode__(self):
        return self.first_name +" "+ self.last_name

    def as_json(self):
        return dict(
            id = self.pk,
            facebook_id = self.facebook_id,
            first_name = self.first_name,
            last_name = self.last_name,
            full_name = self.first_name +" "+ self.last_name,
            email = self.email,
            age = self.age(),
            birthday = self.birthday.isoformat(),
            created = self.created.isoformat())



class City(models.Model):
    city_name = models.CharField(max_length=50, db_index=True, unique=True)

    def __unicode__(self):
        return self.city_name

    def as_json(self):
        return dict(
            id = self.pk,
            city_name = self.city_name)



class Street(models.Model):
    city = models.ForeignKey(City)
    street_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        unique_together = (("city", "street_name"),)

    def __unicode__(self):
        return self.street_name

    def as_json(self):
        
        return dict(
            id = self.pk,
            street_name = self.street_name,
            city = self.city.city_name)


class Address(models.Model):
    street_num = models.IntegerField()
    street = models.ForeignKey(Street)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.street.street_name + ' ' + str(self.street_num) + ', ' + self.city.city_name

    def as_json(self):
        return dict(
            id = self.pk,
            street = self.street.street_name,
            streetNum = self.street_num,
            city = self.city.city_name)
        

class SP(models.Model):
    # CATEGORIES:
    MEDICAL = 'medical'
    RESTAURANTS = 'restaurants'
    SHOPPING = 'shopping'
    PUBLIC_SERVICES = 'public_services'
    TRANSPORTATION = 'transportation'
    HELP = 'help'

    CATEGORY_CHOICES = (
        (MEDICAL, 'Medical'),
        (RESTAURANTS, 'Restaurants'),
        (SHOPPING, 'Shopping'),
        (PUBLIC_SERVICES, 'Public Services'),
        (TRANSPORTATION, 'Transportation'),
        (HELP, 'Help'),
    )


    # Fields:
    sp_address = models.ForeignKey(Address)
    name = models.CharField(max_length=100, db_index=True)
    desc = models.CharField(max_length=225, blank = True)
    longitude = models.DecimalField(max_digits=7, decimal_places=7, db_index=True, blank=True, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=7, db_index=True, blank=True, null=True)
    phone = models.CharField(max_length=13, db_index=True, blank = True)
    is_verified = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, db_index=True, blank = True)
    category = models.CharField(max_length=45, choices=CATEGORY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank = True)
    rank =  models.BigIntegerField(default=0, blank=True)
    voters = models.IntegerField(default=0, blank=True)
    # Accessibility Fields
    toilets = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    entrance = models.BooleanField(default=False)
    facilities = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    """
    TODO: Add Accecability fileds:
    entrance : ramp, wideCoridors, wideEntrance
    facilities: allowServicePets, counters, fittingRooms: handbars, chair/bench
    Toilets: handicapToilets, handbars, accecible sink
    """

    # Add Photos Support

    # Functions
    def address(self):
        return unicode(self.sp_address)

    def __unicode__(self):
        return self.name + ', ' + self.address()

    #Json Parsers
    def as_json(self, withReviews):
        addressText = unicode(self.address())

        response= dict(
            id = self.pk,
            name = self.name,
            desc = self.desc,
            address = addressText,
            longitude = self.longitude,
            latitude = self.latitude,
            phone = self.phone,
            is_verified =self.is_verified,
            discount = self.discount,
            category =self.category,
            website = self.website,
            toilets= self.toilets,
            elevator = self.elevator,
            entrance = self.entrance,
            facilities = self.facilities,
            parking =self.parking,
            )

        if (withReviews):
            reviews = self.review_set.all()
            reviewsList = list()
            for review in reviews:
                reviewsList.append(review.as_json())
            print reviewsList
            response['reviews'] = reviewsList

        return response

class Review(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField(blank = True)
    likes = models.IntegerField(default=0, blank= True, db_index=True)
    sp = models.ForeignKey(SP)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def as_json(self):
        return dict(
            id = self.pk,
            title = self.title,
            content = self.content,
            likes = self.likes,
            created = self.created.isoformat(),
            user = self.user.as_json())
