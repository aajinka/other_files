from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Zanr(models.Model):
    nazev_zanru = models.CharField(max_length=80, verbose_name="Žánr")

    def __str__(self):
        return "Název_žánru: {0}".format(self.nazev_zanru)

    class Meta:
        verbose_name = "Žánr"
        verbose_name_plural = "Žánry"

class Tag(models.Model): # vytvoříme třídu tagy, pro příklad vazby m:n
    tag_title = models.CharField(max_length=50, verbose_name="Tagy")

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagy"

class Film(models.Model):
    nazev = models.CharField(max_length=200, verbose_name = "Název filmu")
    rezie = models.CharField(max_length=180, verbose_name = "Režie")
    zanr = models.ForeignKey(Zanr, on_delete=models.SET_NULL, null=True, verbose_name = "Žárn") # nová vlastnost tagy
    # Vztah mezi filmem a tagem 
    tagy = models.ManyToManyField(Tag)
    def __init__(self, *args, **kwargs):
        super(Film, self).__init__(*args, **kwargs) # konstruktor předka pro korektnost

    def __str__(self):
        # nové - tag-film
        tags = [i.tag_title for i in self.tagy.all()] # seznam tagů pro převod na text
        return "Název:{0} | Režie: {1} | Žánr: {2} | Tagy: {3}".format(self.nazev, self.rezie, self.zanr, tags)
    
    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"

class UzivatelManager(BaseUserManager):
    # Vytvoří uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user
    # Vytvoříme admina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user
# Model rozšiřuje standardní Django model. V metodě create_user() namísto Uzivatel vytváříme self.model. 
# Ten v této třídě odkazuje na náš model uživatele, jelikož jsme nastavili objects pro tento manager. 
# Pokud vám pojem objects nic neříká, vzpomeňte si, jak jsme v Django interaktivním shellu zobrazovali veškeré filmy uložené v DB Film.objects.all(). 
# U našeho uživatele jen tento manažer přepíšeme a tím docílíme toho, že model Uzivatel bude používat náš vlastní manažer.

class Uzivatel(AbstractBaseUser):
        email = models.EmailField(max_length=300, unique=True)
        is_admin = models.BooleanField(default=False)

        class Meta:
            verbose_name = "uživatel"
            verbose_name_plural = "uživatelé"

        objects = UzivatelManager()

        USERNAME_FIELD = "email"

        def __str__(self):
            return "email: {}".format(self.email)
        
        @property
        def is_staff(self):
            return self.is_admin
        
        def has_perm(self, perm, obj=None):
            return True 
        
        def has_module_perms(self, app_label):
            return True 
            