from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import wiki_forms #import from wiki_forms.py
from . import util
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    if request.method == "POST":
        form = wiki_forms.NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]

            if query in util.list_entries():
                return HttpResponseRedirect(reverse('encyclopedia:entry', kwargs={'entry_name':query}))
            
            return render(request, "encyclopedia/results.html" , {
                "form": wiki_forms.NewSearchForm(),
                "results":[entry for entry in util.list_entries() if query in entry]
            })
    
    return render(request, "encyclopedia/index.html", {
        "form":wiki_forms.NewSearchForm(),
        "entries": util.list_entries()
    })




def show_entry(request, entry_name):
    contents = util.get_entry(entry_name)

    if contents:
        html_contents = markdowner.convert(contents)
        return render(request, "encyclopedia/show_entry.html", {
            "form":wiki_forms.NewSearchForm(),
            "contents": html_contents,
            "entry_name": entry_name
        })
    
    return render(request, "encyclopedia/not_found.html", {
        "form":wiki_forms.NewSearchForm(),
    })




def create_entry(request):
    if request.method == "POST":
        entry_form = wiki_forms.NewEntryForm(request.POST)

        # check form validity server-side
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]       #title from form
            contents = entry_form.cleaned_data["contents"] #contents from form

            if title in util.list_entries():      #check if entry already exist
                return render(request,"encyclopedia/create_entry.html", {
                "form":wiki_forms.NewSearchForm(),
                "entry_form":entry_form,
                "entry_exists":True,
                "entry_title":title
            })
            
            #save entry and redirection
            util.save_entry(title, contents)
            return HttpResponseRedirect(reverse('encyclopedia:entry', kwargs={'entry_name':title}))
        
        else:
            return render(request,"encyclopedia/create_entry.html", {
                "form":wiki_forms.NewSearchForm(),
                "entry_form":entry_form,
                "entry_exists":False,
                "entry_title":None
            })
    
    #if not post
    return render(request,"encyclopedia/create_entry.html", {
        "form":wiki_forms.NewSearchForm(),
        "entry_form":wiki_forms.NewEntryForm(),
        "entry_exists":False,
        "entry_title":None
    })




def edit_entry(request, entry_name):
    if request.method=="POST": #if post save the edit
        edit_form = wiki_forms.NewEditForm(request.POST)
        if edit_form.is_valid():
            contents = edit_form.cleaned_data["contents"]
            util.save_entry(entry_name, contents)
            return HttpResponseRedirect(reverse('encyclopedia:entry', kwargs={'entry_name':entry_name}))
    
    # show edit form
    contents = util.get_entry(entry_name)
    return render(request, "encyclopedia/edit_entry.html", {
        "form":wiki_forms.NewSearchForm(),
        "entry_name":entry_name,
        "edit_form": wiki_forms.NewEditForm(initial={"contents":contents})
    })



def random(request):
    import random    #import random library
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":entry}))
