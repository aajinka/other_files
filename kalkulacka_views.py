from django.shortcuts import render

from . import nas_model # Import našeho modelu..

# Metoda pro obsluhu uživatelského požadavku
def kalkulacka(request):
    error_msg=None
    vysledek=None 
    # Validace metody, v případě výjimky vrátí HTML templát s chybovou hláškou
    if request.method == "POST":
        try:
            float(request.POST["a"])
            float(request.POST["b"])
        except:
            error_msg = "A nebo B není číslo!"
            return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))

        # .. předat data našemu modelu a výsledek předat šabloně

        if (float(request.POST["b"]) == 0 and request.POST["operator"] == "/" ):
            error_msg = "Chyba dělení nulou."
            return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))
        if (request.POST["operator"] == "+"):
            vysledek = nas_model.secti(request.POST["a"], request.POST["b"]) 
        elif (request.POST["operator"] == "-"):
            vysledek = nas_model.odecti(request.POST["a"], request.POST["b"]) 
        elif (request.POST["operator"] == "/"):
            vysledek = nas_model.podil(request.POST["a"], request.POST["b"]) 
        elif (request.POST["operator"] == "*"):
            vysledek = nas_model.soucin(request.POST["a"], request.POST["b"]) 
        else: 
            error_msg = "Něco se pokazilo:(."
            return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))
    return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))