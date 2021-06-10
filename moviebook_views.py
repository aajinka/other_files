from django.shortcuts import render, redirect, reverse 

#from django.views.generic import ListView 
from django.views import generic # naimportujeme generic views 

from .models import Film, Uzivatel # a samotné modely
from .forms import FilmForm, UzivatelForm, LoginForm # import pro formulář
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # omezení odhlášení, instalováno v settins.py
from django.contrib.auth.mixins import LoginRequiredMixin # zablokování přístupu nepřihlášeným uživatelů, hodit na login-url

class FilmIndex(generic.ListView): # view není již jen pouhá metoda, ale třída dědící z generic.ListView
    template_name = "moviebook/film_index.html" # dědí z této šablony
    context_object_name = "filmy" # tímto jménem budeme volat list objektů v templátu


# tato funkce nám získává list filmů seřazených od posledně přidaného po nejstarší id (9.8.7...)
    def get_queryset(self):
        return Film.objects.all().order_by("-id")
      
class CurrentFilmView(generic.DetailView): 
    model = Film
    template_name = "moviebook/film_detail.html"

    # metoda pro výpis formuláře upraveného pro editaci a smazání(filmovy_detail.html)
    def get(self, request, pk):
        try:
            film =  self.get_object()
        except:
            return redirect("filmovy_index")
        return render(request, self.template_name, {"film":film})

    # metoda pro odstranění filmu/editace, po kliknutí
    def post(self, request, pk):
        if request.user.is_authenticated: # autentizace a edit
            if "edit" in request.POST:
                return redirect("edit_film", pk=self.get_object().pk)
            else:
                if not request.user.is_admin: # pokud nejsi admin, nemažeš
                    messages.info(request, "Nemáš právo pro smazání filmu!")
                    return redirect(reverse("filmovy_index"))
                else: 
                    self.get_object().delete()
        return redirect(reverse("filmovy_index"))

    # + vytvoření nového view pro editaci, class EditFilm(plus přidat do url) 

class CreateFilm(LoginRequiredMixin, generic.edit.CreateView): # naimportovat LRMixin

    form_class = FilmForm
    template_name = "moviebook/create_film.html"

# Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin: # přidávat filmy může jen admin
            messages.info(request, "Nemáš práva pro přidávání filmů!")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

# Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nový film; pokud není, zobrazí chybovou hlášku
    def post(self, request):
        if not request.user.is_admin: # přidávat filmy může jen admin
            messages.info(request, "Nemáš práva pro přidávání filmů!")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render (request, self.template_name, {"form":form}) 

#def index(request):
    #return render(request, "moviebook/index.html", dict(nazev_filmu="Strážci Galaxie", zanr="Fantasy", hodnoceni="11/10"))

class EditFilm(LoginRequiredMixin, generic.edit.CreateView): # naimportovat LRMixin

    form_class = FilmForm
    template_name = "moviebook/create_film.html"

    def get(self, request, pk):
        if not request.user.is_admin: # editovat filmy může jen admin
            messages.info(request, "Nemáš práva pro úpravu filmu!")
            return redirect(reverse("filmovy_index"))
        try:
            film = Film.objects.get(pk=pk)
        except:
            messages.error(request, "Tento film neexistuje!")
            return redirect("filmovy_index")
        form = self.form_class(instance=film)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin: # editovat filmy může jen admin
            messages.info(request, "Nemáš práva pro úpravu filmu!")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            nazev = form.cleaned_data["nazev"]
            rezie = form.cleaned_data["rezie"]
            zanr = form.cleaned_data["zanr"]
            tagy = form.cleaned_data["tagy"]
            try:
                film = Film.objects.get(pk=pk)
            except:
                messages.error(request, "Tento film neexistuje!")
                return redirect("filmovy_index")
            film.nazev = nazev
            film.rezie = rezie
            film.zanr = zanr
            film.tagy.set(tagy)
            film.save()
        # return render(request, self.template_name, {"form":form})
        return redirect("filmovy_detail", pk=film.id)

class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "moviebook/user_form.html"

    def get(self, request):
        if request.user.is_authenticated: # ošetření přihlášení/registrace
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("filmovy_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request): # zpracuje odeslaný formulář
        if request.user.is_authenticated: # ošetření registrace/přihlášení
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse, "filmovy_index")
        form = self.form_class(request.POST)
        if form.is_valid(): # musí ověřit validnost
            uzivatel = form.save(commit=False) # pokud je validní, uloží uživatele, ale commit=False, protože chceme ještě nastavit heslo
            # pokud uložím bez hesla, tj commit=True, heslo by se nezahashovalo
            password = form.cleaned_data["password"] # nastavíme heslo jako hash
            uzivatel.set_password(password)
            uzivatel.save() # uložíme uzivatele
            login(request, uzivatel)
            return redirect ("filmovy_index")
             
        return render(request, self.template_name, {"form": form})

class UzivatelViewLogin(generic.edit.CreateView): # login 
    form_class = LoginForm
    template_name = "moviebook/user_form.html"

    def get(self, request):
        if request.user.is_authenticated: # ošetření registrace/přihlášení
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse, "filmovy_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if request.user.is_authenticated: # ošetření registrace/přihlášení
            messages.info(request, "Už jsi přihlášený, nemůžeš se znovu přihlásit.")
            return redirect(reverse, "filmovy_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect ("filmovy_index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form":form})

    # pro logout použijeme funkci logout() s parametrem request

    def logout_user(self,request):
        if request.user.is_authenticated: # aby nás odhlásil, jen když jsme přihlášení
            logout(request)
              
        else:
            messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
        return redirect(reverse("login"))

