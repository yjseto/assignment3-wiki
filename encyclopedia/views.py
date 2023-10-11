from django.shortcuts import render
import markdown2
from . import util
from .forms import NewEntryForm
from django.http import HttpResponseRedirect

from django.urls import reverse
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, entry):
    # if entry doesn't exist, error page
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/error.html",{
            "message": f"the page for {entry} was not found"
        })

    # if entry exists, fetch markdown for the page
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "body": util.get_entry(entry)
    })

def search(request):
    query = request.POST['q'] # query from search form
    entries = util.list_entries() # list of all entries
    matches = [] # empty list to store partial matches
    if query is not None:
        for entry in entries:
            # if partial match, add entry to partial match list
            if query.lower() in entry.lower():
                matches.append(entry)
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "matches": matches
    })
    
# create a new encyclopedia page
def new(request):
    # display empty entry form
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })
    # else if request method POST
    else:
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # save title and entry
            title = form.cleaned_data["title"]
            body = form.cleaned_data["newentry"]
            alltitles = util.list_entries()

            # return error if the title entered already exists
            for t in alltitles:
                if title.lower() == t.lower():
                    return render(request, "encyclopedia/error.html", {
                        "message": f"the title {t} already exists"
                    })
            # save valid entry and redirect to the new page
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("title", kwargs={
                "entry": title
                }))
        else:
            # return invalid form back to user
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

# edit any encyclopedia entry
def edit(request, title):
    if request.method =="GET":
        body = util.get_entry(title)
        preform = NewEntryForm(initial={'title': title, 'newentry': body})
        return render(request, "encyclopedia/edit.html", {
            "preform": preform
        })    
    # if POST, save entry
    else:
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # save cleaned title and entry
            title = form.cleaned_data["title"]
            body = form.cleaned_data["newentry"]

            # save entry and redirect to the updated page
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("title", kwargs={
                "entry": title
            }))
        else:
            # return invalid form back to user
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
                
def delete(request, title):
    if request.method =="GET":
        body = util.get_entry(title)
        if body is not None:
            util.delete_entry(title)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": util.get_entry(title)
        })    
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": util.get_entry(title)
        })

# display any random entry
def random_entry(request):
    entrylist = util.list_entries() # all entry titles
    num = random.randrange(len(entrylist)) # pick a random number 1-total
    pick = entrylist[num] # get random title
    return HttpResponseRedirect(reverse("title", kwargs={
                "entry": pick
            }))
    


def md_html(request):
    # Read Markdown content from your file or database
    markdown_content = "CSS.md"

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Pass the HTML content to your template
    return render(request, 'entry.html', {'html_content': html_content})



