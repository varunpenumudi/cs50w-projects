from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlisted_users")
    pass


# New Models
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings") # who creates the listing
    title = models.CharField(max_length=64) 
    description = models.TextField()             
    image_url = models.URLField(max_length=200, blank=True) 
    category = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    # get the maximum price of all the bids prices placed on listing.
    def get_max_bid(self):
        return max([ bid.bid_price for bid in self.bids.all() ]) if self.bids.all() else 0
    
    # get the user who bidded for max price on this listing.
    def get_max_bid_user(self):
        max_bid =  max(self.bids.all(), key=lambda x: x.bid_price )
        return max_bid.user
    
    # get number of bids placed on this listing.
    def get_bid_count(self):
        return self.bids.all().count()

    def __str__(self) -> str:
        return f"{self.title.upper()} by {self.user.username.title()} at   price: ${self.get_max_bid()}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    bidded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f" {self.id} bid by {self.user} on {self.listing.title} "

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    content = models.TextField()

    def __str__(self) -> str:
        return f"{self.pk} {self.content} by {self.user}"