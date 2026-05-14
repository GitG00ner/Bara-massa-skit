import os
import json
import pygame
import cmath
import matplotlib.pyplot as plt
import numpy as np


def update_plot(a, b, c, event_ax, line, fig):
    try:
        # 1. Get the new window limits
        xlim = event_ax.get_xlim()
        
        # 2. Calculate new data for exactly what is visible
        x_new = np.linspace(xlim[0], xlim[1], 2000)
        y_new = a*x_new**2 + b*x_new + c
        
        # 3. Update the line
        line.set_data(x_new, y_new)
                
        # 5. Redraw the canvas
        fig.canvas.draw_idle()
    except:
        # This catches "in-progress" errors during fast zooming
        pass

def andragradsfunktion_visualisering(a, b, c, n1, n2):
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.linspace(-10, 10, 1000)
    y = a*x**2 + b*x + c
    
    
    line, = ax.plot(x, y, color='blue', lw=2)

    plt.title(f"Andragradsfunktion\nNollställen: {n1} och {n2}")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.axhline(0, color='black', lw=1) # x-axis
    plt.axvline(0, color='black', lw=1) # y-axis

    ax.callbacks.connect('xlim_changed', lambda e: update_plot(a, b, c, e, line, fig))

    plt.show()

def nollstellen(a, b, c):
    if a == 0:
        print("Inte en andragradsfunktion!")
        return None, None
    
    # Standard pq-formel/abc-formel logic
    d = (b**2) - (4*a*c)
    x1 = (-b + cmath.sqrt(d)) / (2*a)
    x2 = (-b - cmath.sqrt(d)) / (2*a)

    andragradsfunktion_visualisering(a, b, c, x1, x2)
    return x1, x2

def backgroundmusic():
    pygame.mixer.init()
    pygame.mixer.music.load("Miniräknare\energysound-stomp-drum-percussion-513744 (1).mp3")
    pygame.mixer.music.play(-1)  # Spela i loop

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def sparade_svar():
    if os.path.exists('Miniräknare\spara_svar.json'):
        try:
            with open('Miniräknare\spara_svar.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def kolla_input(input, svar_lista):
    svar = ["a", "awnser", "svar", "s", ]

    tempinputlist = input.split()

    if input in svar:
        return svar_lista[-1]

    try:
        return float(input)
        
    except:
        return None

def basic_kalk(o, svar_lista):
    num1, num2 = num_sammling(svar_lista)

    if o == "+":
        svar_lista.append(num1 + num2)
        return num1 + num2
    
    elif o == "-":
        svar_lista.append(num1 - num2)
        return num1 - num2
    
    elif o == "*":
        svar_lista.append(num1 * num2)
        return num1 * num2
    
    elif o == "/":
        if num2 != 0:
            svar_lista.append(num1 / num2)
            return num1 / num2
    
        else:
            print("Error: division med 0")
            return None

def num_sammling(svar_lista):
        num1 = kolla_input(input("Skriv det första talet: "), svar_lista)
        num2 = kolla_input(input("Skriv det andra talet: "), svar_lista)

        return num1, num2

def uppdelning(input_string):
    """Delar upp inmatningen i lista med tal och operatorer."""

    input_string = input_string.replace("+", " + ")
    input_string = input_string.replace("-", " - ")
    input_string = input_string.replace("*", " * ")
    input_string = input_string.replace("/", " / ")
    input_string = input_string.split()
    return input_string


def konvertering(tal, svar_lista):
    """Konverterar tal och ersätter 'svar' med senaste svaret."""
    for i in range(len(tal)):
        if tal[i] not in ["+", "-", "*", "/"]:
            tal[i] = kolla_input(tal[i], svar_lista)
    return tal

def multiplikation_divition(tal):
    """Hanterar * och / (högre prioritet)."""
    i = 0
    while i < len(tal):
        if tal[i] == "*":
            resultat = tal[i-1] * tal[i+1]
            tal[i-1:i+2] = [resultat]
            i = 0
            continue
        elif tal[i] == "/":
            if tal[i+1] == 0:
                print("Error: division med 0")
                return False
            resultat = tal[i-1] / tal[i+1]
            tal[i-1:i+2] = [resultat]
            i = 0
            continue
        i += 1
    return True

def addition_subtraktion(tal):
    """Hanterar + och - (lägre prioritet)."""
    i = 0
    while i < len(tal):
        if tal[i] == "+":
            resultat = tal[i-1] + tal[i+1]
            tal[i-1:i+2] = [resultat]
            i = 0
            continue
        elif tal[i] == "-":
            resultat = tal[i-1] - tal[i+1]
            tal[i-1:i+2] = [resultat]
            i = 0
            continue
        i += 1

def intelligent_calculator(svar_lista):
    """Intelligent kalkylator för komplexa matematikproblem."""
    clear()
    input_string = input("Skriv ditt matematikproblem: ")
    
    try:
        tal = uppdelning(input_string)

        tal = konvertering(tal, svar_lista)
        
        if not multiplikation_divition(tal):
            return
        
        addition_subtraktion(tal)
        
        if isinstance(tal[0], (int, float)):
            print(f"Svar: {tal[0]}")
            svar_lista.append(tal[0])
            
    except:
        print("Felaktig input.")

def mainloop():
    
    clear()
    
    musik = input("Vill du ha musik? (ja/nej) ")
    if musik == "ja":
        backgroundmusic()

    svar_lista = sparade_svar()

    run=True

    spara_inte_varde = False

    clear()

    while run:
        #snabbt och smidigt sparar svaren till json på direkten, det är vad jag kallar code so clean it sparkles!
        if spara_inte_varde == False:
            with open('Miniräknare\spara_svar.json', 'w') as f:
                json.dump(svar_lista, f, indent=2)
        else:
            spara_inte_varde = False


        metod = input("Vilken metod vill du köra? (1 (addition), 2 (subtration), 3 (multiplication), 4 (division), 5 (tidigare svar), 6 (intelligent), 7 (nollpunkter) eller q för att avsluta) ")
        
        if metod == "1":
            svar = basic_kalk("+", svar_lista)
            print(f"Svar: {svar}")

        elif metod == "2":
            svar = basic_kalk("-", svar_lista)
            print(f"Svar: {svar}")

        elif metod == "3":
            svar = basic_kalk("*", svar_lista)
            print(f"Svar: {svar}")


        elif metod == "4":
            svar = basic_kalk("/", svar_lista)
            print(f"Svar: {svar}")

        elif metod == "q":

            run = False

        elif metod == "5":

            if svar_lista:
                for i, result in enumerate(svar_lista, start=1):
                    print(f"Svar {i}: {result}")

            else:
                print("Inga tidigare svar att visa.")
        
        elif metod == "6":
            intelligent_calculator(svar_lista)

        elif metod == "7":
            a = kolla_input(input("ax^2+bx+c\n  Skriv a: "), svar_lista)
            b = kolla_input(input("ax^2+bx+c\n  Skriv b: "), svar_lista)
            c = kolla_input(input("ax^2+bx+c\n  Skriv c: "), svar_lista)

            svar_lista.append(nollstellen(a, b, c))
            x1, x2 = nollstellen(a, b, c)
            if x1 is not None and x2 is not None:
                print(f"Nollpunkter: {x1} och {x2}")
            spara_inte_varde = True

        else:
            print("Ogiltig metod. Försök igen.")

if __name__ == "__main__":
    mainloop()