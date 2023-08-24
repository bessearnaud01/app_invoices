def afficher_kwargs(**kwargs):
    for cle, valeur in kwargs.items():
        print(f"{cle} : {valeur}")

afficher_kwargs(a=1, b=2, c=3,e=8)
