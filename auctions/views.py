# All relevant imports
# References: < Havrard CS50 and Zach Barlow> 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django import forms
# Handles client side Error exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# import models from current directory
from .models import User, Auction, Bid, Comment, Watchlist


class CreateListingForm(forms.ModelForm):
    
    title = forms.CharField(label="Title", max_length=20, required=True, widget=forms.TextInput(attrs={
                                                                            "autocomplete": "off",
                                                                            "aria-label": "title",
                                                                            "class": "form-control"
                                                                        }))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
                                    'placeholder': "Tell more about the product",
                                    'aria-label': "description",
                                    "class": "form-control"
                                    }))
    image_url = forms.URLField(label="Image URL", required=True, widget=forms.URLInput(attrs={
                                        "class": "form-control"
                                    }))

    category = forms.ChoiceField(required=True, choices=Auction.CATEGORY, widget=forms.Select(attrs={
                                        "class": "form-control"
                                    }))

    class Meta:
        model = Auction
        fields = ["title", "description", "category", "image_url"]

class BidForm(forms.ModelForm):
    """Creates form for Bid model."""
    class Meta:
        model = Bid
        fields = ["bid_price"]
        labels = {
            "bid_price": _("")
        }
        widgets = {
            "bid_price": forms.NumberInput(attrs={
                "placeholder": "Bid",
                "min": 0.01,
                "max": 100000000000,
                "class": "form-control"
            })
        }

class CommentForm(forms.ModelForm):
    """Creates form for Comment model."""
    class Meta:
        model = Comment
        fields = ["comment"]
        labels = {
            "comment": _("")
        }
        widgets = {
            "comment": forms.Textarea(attrs={
                "placeholder": "Comment here",
                "class": "form-control",
                "rows": 1
            })
        }

# ----------------------------------------------------------------------
# ------------------------------  Views  -------------------------------
# ----------------------------------------------------------------------
def index(request):
    """Main view: shows all listings."""
    # Get all auctions descending
    auctions = Auction.objects.filter(closed=False).order_by("-publication_date")

    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

# @login_required decorator ensure that only a user who is logged in can access that view.
@login_required(login_url="auctions:login")

# display functions on sale
def user_panel(request):
    
    # Helpers
    all_distinct_bids =  Bid.objects.filter(user=request.user.id).values_list("auction", flat=True).distinct()
    won = []

    # Get auctions currently being sold by the user
    selling = Auction.objects.filter(closed=False, seller=request.user.id).order_by("-publication_date").all()

    # Get auction sold by the user
    sold = Auction.objects.filter(closed=True, seller=request.user.id).order_by("-publication_date").all()

    # Get auctions currently being bid by the user
    bidding = Auction.objects.filter(closed=False, id__in = all_distinct_bids).all()

    # Get auctions won by the user
    for auction in Auction.objects.filter(closed=True, id__in = all_distinct_bids).all():
        highest_bid = Bid.objects.filter(auction=auction.id).order_by('-bid_price').first()

        if highest_bid.user.id == request.user.id:
            won.append(auction)

    return render(request, "auctions/user_panel.html", {
        "selling": selling,
        "sold": sold,
        "bidding": bidding,
        "won": won
    })

# @login_required decorator ensure that only a user who is logged in can access that view.
@login_required(login_url="auctions:login")
def create_listing(request):

    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Get all data from the form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]

            # Save a record
            auction = Auction(
                seller = User.objects.get(pk=request.user.id),
                title = title,
                description = description,
                category = category,
                image_url = image_url
            )
            auction.save()
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    return render(request, "auctions/create_listing.html", {
        "form": CreateListingForm(),
    })

# details of a single item
def listing_page(request, auction_id):

    # check for current action
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "Auction id doesn't exist"
        })

    # Information about bids
    bid_amount = Bid.objects.filter(auction=auction_id).count()
    highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid_price').first()

    # Auction shown to only winner
    if auction.closed:
        if highest_bid is not None:
            winner = highest_bid.user

            # Diffrent views for different users
            if request.user.id == auction.seller.id:
                return render(request, "auctions/sold.html", {
                    "auction": auction,
                    "winner": winner
                })
            elif request.user.id == winner.id:
                return render(request, "auctions/bought.html", {
                    "auction": auction
                })
        else:
            if request.user.id == auction.seller.id:
                return render(request, "auctions/closed_no_offer.html", {
                    "auction": auction
                })

        return HttpResponse("Error - auction no longer available")
    else:
         # check for auction for particular user after authenticating
        if request.user.is_authenticated:
            watchlist_item = Watchlist.objects.filter(
                    auction = auction_id,
                    user = User.objects.get(id=request.user.id)
            ).first()

            if watchlist_item is not None:
                on_watchlist = True
            else:
                on_watchlist = False
        else:
            on_watchlist = False

        # FFirst get all comments
        comments = Comment.objects.filter(auction=auction_id)

        # CHighest bidder
        if highest_bid is not None:
            if highest_bid.user == request.user.id:
                bid_message = "Your bid is the highest bid"
            else:
                bid_message = "Highest bid made by " + highest_bid.user.username
        else:
            bid_message = None

        return render(request, "auctions/listing_page.html", {
            "auction": auction,
            "bid_amount": bid_amount,
            "bid_message": bid_message,
            "on_watchlist": on_watchlist,
            "comments": comments,
            "bid_form": BidForm(),
            "comment_form": CommentForm()
        })

@login_required(login_url="auctions:login")
def watchlist(request):
    """Watchlist views: shows all auctions that are on user's watchlist."""
    # Save information about the auction and return to login page
    if request.method == "POST":
        # Information about the auction
        auction_id = request.POST.get("auction_id")

        # clean auctions
        try:
            auction = Auction.objects.get(pk=auction_id)
            user = User.objects.get(id=request.user.id)
        except Auction.DoesNotExist:
            return render(request, "auctions/error_handling.html", {
                "code": 404,
                "message": "Auction id doesn't exist"
            })

        # Add/delete from watch list 
        if request.POST.get("on_watchlist") == "True":
            # Delete it from watchlist model
            watchlist_item_to_delete = Watchlist.objects.filter(
                user = user,
                auction = auction
            )
            watchlist_item_to_delete.delete()
        else:
            # Save to watchlist model
            try:
                watchlist_item = Watchlist(
                    user = user,
                    auction = auction
                )
                watchlist_item.save()
            # Make sure it is not duplicated for current user
            except IntegrityError:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Auction is already on your watchlist"
                })
    # redirect user
        return HttpResponseRedirect("/" + auction_id)


    watchlist_auctions_ids = User.objects.get(id=request.user.id).watchlist.values_list("auction")
    watchlist_items = Auction.objects.filter(id__in=watchlist_auctions_ids, closed=False)

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

# @login_required decorator ensure that only a user who is logged in can access that view.
@login_required(login_url="auctions:login")
def bid(request):
    """Bid view: only POST method allowed, handles bidding logic."""
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_price = float(form.cleaned_data["bid_price"])
            auction_id = request.POST.get("auction_id")

            # Avoid negative bids
            if bid_price <= 0:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Bid price must be greater than 0"
                })

            # Confirm auction using try and catch to catch errors
            try:
                auction = Auction.objects.get(pk=auction_id)
                user = User.objects.get(id=request.user.id)
            except Auction.DoesNotExist:
                return render(request, "auctions/error_handling.html", {
                    "code": 404,
                    "message": "Auction id doesn't exist"
                })

            # Ensure bidder isn't seller
            if auction.seller == user:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Seller cannot ne a bidder"
                })

            #  save new bid if current bid isn't highest
            highest_bid = Bid.objects.filter(auction=auction).order_by('-bid_price').first()
            if highest_bid is None or bid_price > highest_bid.bid_price:
                # Add to the database
                new_bid = Bid(auction=auction, user=user, bid_price=bid_price)
                new_bid.save()

                # Update chighest price
                auction.current_price = bid_price
                auction.save()

                #redirect user 
                return HttpResponseRedirect("/" + auction_id)
            else:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Bid too low"
                })
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Invalid Form"
            })
    # Only post allowed
    return render(request, "auctions/error_handling.html", {
        "code": 405,
        "message": "Cannot retrieve form"
    })

# Categories
def categories(request, category=None):
    # Get all categories
    categories_list = Auction.CATEGORY

    # Check for category in list of categories url
    if category is not None:
        if category in [x[0] for x in categories_list]:
            category_full = [x[1] for x in categories_list if x[0] == category][0]

            # Get all auctions from this category to be displayed
            auctions = Auction.objects.filter(category=category, closed=False)
            return render(request, "auctions/category.html", {
                "auctions": auctions,
                "category_full": category_full
            })
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Invalid category"
            })

    return render(request, "auctions/error_handling.html", {
        "code": 404,
        "message": "Page does not existt"
    })

# @login_required decorator ensure that only a user who is logged in can access that view.
@login_required(login_url="auctions:login")
# close auction
def close_auction(request, auction_id):
    # Get current auction if any is available
    # while handling errors
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "The auction you are searching for doesnt't exist"
        })

    # Close auction
    if request.method == "POST":
        auction.closed = True
        auction.save()
    elif request.method == "GET":
        return render(request, "auctions/error_handling.html", {
            "code": 405,
            "message": "Not Allowed"
        })

    # Redirect user  to auction page
    return HttpResponseRedirect("/" + auction_id)

@login_required(login_url="auctions:login")
def handle_comment(request, auction_id):

    # Check if auction if exists
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "The auction you are searching for doesnt't exist"
        })

    # Post user's comment
    # Ensure it's a post method
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Get all available data from form
            comment = form.cleaned_data["comment"]

            # Record comment
            comment = Comment(
                user=User.objects.get(pk=request.user.id),
                comment = comment,
                auction = auction
            )
            comment.save()
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Form is invalid"
            })
        # else if GET handle error
    elif request.method == "GET":
        return render(request, "auctions/error_handling.html", {
            "code": 405,
            "message": "Not Allowed"
        })

    # Redirect client to auction page
    return HttpResponseRedirect("/" + auction_id)

# handles logim
def login_view(request):
    # Ensure it's a post methi=od for security reasons
    if request.method == "POST":
        # Authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # if  successful
        if user is not None:
            login(request, user)

            # if user goes to login required page
            if "again" in request.POST:
                return HttpResponseRedirect(reverse("auctions:" + request.POST.get("again")[1:]))
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password. Try again"
            })
    else:
        return render(request, "auctions/login.html")

# Logs user out through django's logout function
def logout_view(request):
    
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

# Register new user
def register(request):
    # Ensure post
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Confirm that passwords match."
            })


        # If succesful
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already exits"
            })
        login(request, user)
        # redirect to logged in user to homepage
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        # else direct to register page
        return render(request, "auctions/register.html")

# Handle 404 error
def handle_not_found(request, exception):
    return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "Page not found"
        })

