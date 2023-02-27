# Imports
from django.contrib.auth.models import AbstractUser
from django.db import models


# All models

# User model inherited from django's implementation
class User(AbstractUser):

    pass

# auction model contains information about auctions
class Auction(models.Model):
 
# Categories of auctions with string represntation
    MOTORS = "MOT"
    FASHINON = "FAS"
    ELECTRONICS = "ELE"
    COLLECTIBLES_ARTS = "ART"
    HOME_GARDES = "HGA"
    SPORTING_GOODS = "SPO"
    TOYS = "TOY"
    BUSSINES_INDUSTRIAL = "BUS"
    MUSIC = "MUS"

# A list category of tuples, ordered and unchangeable
    CATEGORY = [
        (MOTORS, "Motors"),
        (FASHINON, "Fashion"),
        (ELECTRONICS, "Electronics"),
        (COLLECTIBLES_ARTS, "Collectibles & Art"),
        (HOME_GARDES, "Home & Garden"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys"),
        (BUSSINES_INDUSTRIAL, "Business & Industrial"),
        (MUSIC, "Music"),
    ]

    
    # Create model fields imported from django models class extending sqlite 

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=3, choices=CATEGORY, default=MOTORS)
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "auction"
        verbose_name_plural = "auctions"

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, seller: {self.seller}"


# Bid model contains info about auction, user, date and price
class Bid(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"

    # create string representation Bid model
    def __str__(self):
        return f"{self.user} bid {self.bid_price} $ on {self.auction}"


# information about a single comment, user, on what item, comment and comment date
class Comment(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    # # create string representation of Comment model
    def __str__(self):
        return f"{self.user}, {self.id} commented on {self.auction} "

# Contains all information about items on watchlist
class Watchlist(models.Model):

# Foreign keys references auction and and User
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"
        # Forces to not have auction duplicates for one user
        unique_together = ["auction", "user"]

    # create string representation of Watchlist model
    def __str__(self):
        return f"{self.user} watching {self.auction}  "
