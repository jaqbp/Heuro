from ObjectiveFunction import ObjectiveFunction

if __name__ == "__main__":
    of = ObjectiveFunction()

    # Obliczenie wartości w dowolnym punkcie
    x = of.FunkcjaCelu.Wartosc(1.26, 1.3, 1.1)
    print(x)

    # Wartość referencyjna dla trzech jedynek
    print(of.FunkcjaCelu.Wartosc(1.0, 1.0, 1.0))

    # Optymalizacja w przedziałach [0.5, 1.5] dla każdego z parametrów
    # of.Optymalizacja()
