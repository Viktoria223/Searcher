from django.shortcuts import redirect, render

import main
from web.forms import SearchForm


def main_view(request):
    form = SearchForm()
    is_word = False
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            total_res = main.main(word)
            is_word = True
            is_empty = False
            if len(total_res) == 0:
                is_empty = True
            return render(request, 'web/main.html', {"total_res": total_res, "form": form,
                                                     "is_word": is_word, "is_empty": is_empty})

    return render(request, "web/main.html", {"form": form})
