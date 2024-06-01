from django.contrib import admin
from .models import User,Listing, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_price', 'user', 'listing')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content')

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)