from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingCreationForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        'active_listings': Listing.objects.filter(active=True),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create a Listing
@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form  = ListingCreationForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data['description']
            starting_bid_price = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            category  = form.cleaned_data['category'].strip().lower()

            listing = Listing.objects.create(
                user=request.user, 
                title=title, 
                description = desc, 
                image_url=image_url, 
                category = category,
                active=True
            )

            starting_bid = Bid.objects.create(
                user = request.user,
                listing = listing,
                bid_price = starting_bid_price
            )

            return HttpResponseRedirect(reverse('index'))
        
        return render(request, "auctions/create.html", {"form": ListingCreationForm(request.POST) })
    else:
        return render(request, "auctions/create.html", {"form":ListingCreationForm()})


# view for watchlist page
@login_required(login_url="/login")
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'watchlist': request.user.watchlist.all(),
    })


# Shows listing details and Bid on it
def listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    not_in_watchlist = ( (request.user.is_authenticated) and (not (listing in request.user.watchlist.all())) )

    if request.method == "POST" and request.user.is_authenticated: #bid on item
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        bid_price = float(request.POST['bidprice']) #get bid price from form

        if bid_price <= listing.get_max_bid():
            bid_error_message = " Your bid is too low "
            return render( request, "auctions/show_listing.html", {
                "listing":listing,
                "not_in_watchlist": not_in_watchlist,
                "bid_error_message": bid_error_message,
                "comment_form":CommentForm(),
                "comments": listing.comments.all()
            })
        Bid.objects.create( user=user, listing=listing, bid_price=bid_price )

    return render(request, "auctions/show_listing.html", {
        "listing":listing,
        "comments":listing.comments.all(),
        "not_in_watchlist": not_in_watchlist,
        "comment_form": CommentForm()
    })


# view for categories page
def categories(request):
    categories = Listing.objects.values('category').distinct()
    return render(request, "auctions/categories.html", {
        "categories":categories,
    })


# view for a specific category page
def category(request, category):
    listings = Listing.objects.filter(category = category.strip())
    return render(request, "auctions/category_listings.html", {
        'title':category.title(),
        'listings': listings,
    })


# adds and remove items in user's watchlist 
@login_required(login_url="/login")
def watchlist_operation(request, listing_id):
    if request.method == "POST":
        if request.POST['operation'] == "add":
            listing = Listing.objects.get(pk=listing_id)
            request.user.watchlist.add(listing)
        if request.POST['operation'] == "remove":
            listing = Listing.objects.get(pk=listing_id)
            request.user.watchlist.remove(listing)
        
        return HttpResponseRedirect(reverse( "listing", args=(listing_id, ) ))


# closes a listing by making it inactive
@login_required(login_url="/login")
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))


#saves comment on a listing
@login_required(login_url="/login")
def comment(request, listing_id): 
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment_content = form.cleaned_data['comment']
            listing = Listing.objects.get(pk = listing_id )
            comment = Comment.objects.create( 
                listing = listing,
                user=request.user, 
                content=comment_content, 
            )
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))