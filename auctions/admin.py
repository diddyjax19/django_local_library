"""Contains configuration on how to show all models in admin page."""

from django.contrib import admin
from .models import User, Auction, Bid, Comment, Watchlist

# Register your models here.

# Created custom user tables view for django admin app

#   User model adminis's configuration
class UserAdmin(admin.ModelAdmin):

# Creating list display for user model's admin app
    list_display = ("id", "username", "email", "password")


#   Auction model adminis's configuration
class AuctionAdmin(admin.ModelAdmin):

    # Creating list display for Auction model's admin app
    list_display = ("id", "title", "category", "current_price",
                    "publication_date", "closed", "seller")


#   Bidding model admini's configuration
class BidAdmin(admin.ModelAdmin):
   
   # Creating list display for bid model's admin app
    list_display = ("auction", "user", "bid_price", "bid_date")


#   Comment model admini's configuration
class CommentAdmin(admin.ModelAdmin):
    
    # Creating list display for comment model's admin app
    list_display = ("auction", "user", "comment")


#   UWatchlist model admini's configuration
class WatchlistAdmin(admin.ModelAdmin):
   
   # Creating list display for user watchlist's admin app
    list_display = ("auction", "user")

# Register all models to the user admin site
admin.site.register(User, UserAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
