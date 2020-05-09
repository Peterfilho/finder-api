import numpy as np
from json import JSONEncoder
import json

#search = np.array([(-66,-76,-78,-62,-79,-81)]) #busca B6A retorna (B6B, B6C, e B10.5)
#search = np.array([(-73,-73,-77,-53,-70,-78)]) #busca B6B retorna (B6A, B6B, B6C, B10.5)
#search = np.array([(-70,-60,-61,-69,-78,-72)]) #busca B9B retorna (B9B)
#search = np.array([(-100,-67,-63,-49,-53,-48)]) #busca WC-M retorna (WC-M)
#search = np.array([(-57,-63,-63,-64,-100,-100)]) #busca B10.2 retorna (B104)
#search = np.array([(-100,-72,-74,-59,-79,-100)]) #busca B8B retorna (B8A)

def localize(aux1, aux2, aux3, aux4, aux5, aux6):

    search = np.array([(aux1,aux2,aux3,aux4,aux5,aux6)], dtype=np.int_)

    B1A = np.array([(-46,-78,-72,-70,-81,-59)])     #B1A
    B1B = np.array([(-100,-82,-85,-100,-76,-55)])   #B1B
    B1C = np.array([(-100,-100,-100,-78,-100,-58)]) #B1C
    B2A = np.array([(-100,-88,-100,-100,-100,-60)])  #B2A
    B2B = np.array([(-100,-78,-79,-80,-80,-59)])     #B2B
    B3A = np.array([(-100,-100,-100,78,-77,-57)])    #B3A
    B3B = np.array([(-100,-100,-100,-80,-80,-52)])   #B3B
    B4A = np.array([(-77,-100,-84,-75,-72,-72)])    #B4A
    B4B = np.array([(-78,-81,-80,-72,-70,-67)])     #B4B
    B4C = np.array([(-76,-76,-81,-67,-62,-67)])     #B4C
    B5A = np.array([(-100,-76,-80,-67,-61,-69)])    #B5A
    B5B = np.array([(-100,-79,-80,-68,-59,-71)])    #B5B
    B6A = np.array([(-77,-81,-78,-62,-76,-80)])     #B6A
    B6B = np.array([(-68,-75,-76,-54,-73,-74)])     #B6B
    B6C = np.array([(-72,-73,-72,-62,-72,-75)])     #B6C
    B7A = np.array([(-100,-78,-78,-65,-74,-78)])    #B7A
    B7B = np.array([(-100,-81,-77,-69,-74,-76)])    #B7B
    B8A = np.array([(-100,-77,-75,-66,-81,-100)])    #B8A
    B8B = np.array([(-82,-74,-76,-64,-80,-100)])     #B8B
    B9A = np.array([(-73,-66,-62,-69,-76,-100)])     #B9A
    B9B = np.array([(-70,-61,-63,-69,-78,-75)])      #B9B
    B9C = np.array([(-70,-57,-75,-75,-100,-79)])     #B9C
    B101 = np.array([(-63,-73,-70,-68,-100,-85)])     #B10.1
    B102 = np.array([(-57,-70,-65,-70,-78,-81)])      #B10.2
    B103 = np.array([(-56,-70,-67,-75,-100,-100)])    #B10.3
    B104 = np.array([(-56,-65,-72,-72,-100,-100)])    #B10.4
    B105 = np.array([(-64,-75,-78,-60,-76,-76)])      #B10.5
    B11A = np.array([(-78,-52,-73,-73,-78,-76)])      #B11A
    B11B = np.array([(-77,-58,-68,-74,-100,-78)])     #B11B
    B11C = np.array([(-83,-67,-82,-78,-79,-79)])      #B11C
    B12A = np.array([(-63,-56,-74,-77,-100,-83)])     #B12A
    B12B = np.array([(-67,-63,-77,-79,82,-100)])      #B12B
    B12C = np.array([(-72,-64,-77,-78,-100,-78)])     #B12C
    WCM = np.array([(-100,-70,-68,-55,-53,-55)])     #WC-M
    WCF = np.array([(-100,-76,-80,-78,-71,-60)])     #WC-F
    C1 = np.array([(-100,-61,-69,-61,-61,-43)])     #C1
    C2 = np.array([(-100,-48,-59,-53,-49,-52)])     #C2
    C3 = np.array([(-67,-58,-60,-48,58,-57)])       #C3
    C4 = np.array([(-55,-46,-57,-52,-54,-55)])      #C4
    C5 = np.array([(-100,-48,-60,-58,-64,-57)])      #C5

    candidatos = [B1A, B1B, B1C, B2A, B2B, B3A, B3B, B4A, B4B, B4C, B5A, B5B, B6A, B6B, B6C, B7A, B7B, B8A, B8B, B9A, B9B, B9C, B101, B102, B103, B104, B105, B11A, B11B, B11C, B12A, B12B, B12C, WCM, WCF, C1, C2, C3, C4, C5]
    margem_erroP = 10.0
    margem_erroN = -10.0

    distancias = candidatos[::] - search # Avalia a distância de cada vetor para o vetor de busca.
    #print(distancias)
    #input("Press Enter to continue...")

    avaliar_dist = np.where(np.absolute(distancias) < margem_erroP, True, False) # Localiza em quais posições dos vetores de distância a margem de erro é satisfeita.
    avaliar_distN = np.where(np.absolute(distancias) < margem_erroN, True, False) # Localiza em quais posições dos vetores de distância a margem de erro é satisfeita.
    #print(avaliar_distN)
    #input("Press Enter to continue...")

    vetores_aprovados = avaliar_dist.all(axis=2) # Marca Verdadeiro se toda a linha tem valores Verdadeiros.
    vetores_aprovados += avaliar_distN.all(axis=2)
    #print(vetores_aprovados)
    #input("Press Enter to continue...")

    posicao_aprovados = np.array(np.where(vetores_aprovados== True)[0]) # Grava a posição dos vetores dentro da margem de erro.
    #print(posicao_aprovados)
    #input("Press Enter to continue...")

    print("---- Resultado ----")
    print()
    print("Busca: {}".format(search))
    print("Resultado: ")
    local = ""
    for x in posicao_aprovados:
        print(candidatos[x])

        here = candidatos[x][-1]
        print("Melhor resultado:")
        print(here)


        if posicao_aprovados[0] == 0:
            print("Local: B1A")
            local = "B1A"
        elif posicao_aprovados[0] == 1:
            print("Local: B1B")
            local = "B1B"
        elif posicao_aprovados[0] == 2:
            print("Local: B1C")
            local = "B1C"
        elif posicao_aprovados[0] == 3:
            print("Local: B2A")
            local = "B2A"
        elif posicao_aprovados[0] == 4:
            print("Local: B2B")
            local = "B2B"
        elif posicao_aprovados[0] == 5:
            print("Local: B3A")
            local = "B3A"
        elif posicao_aprovados[0] == 6:
            print("Local: B3B")
            local = "B3B"
        elif posicao_aprovados[0] == 7:
            print("Local: B4A")
            local = "B4A"
        elif posicao_aprovados[0] == 8:
            print("Local: B4B")
            local = "B4B"
        elif posicao_aprovados[0] == 9:
            print("Local: B4C")
            local = "B4C"
        elif posicao_aprovados[0] == 10:
            print("Local: B5A")
            local = "B5A"
        elif posicao_aprovados[0] == 11:
            print("Local: B5B")
            local = "B5B"
        elif posicao_aprovados[0] == 12:
            print("Local: B6A")
            local = "B6A"
        elif posicao_aprovados[0] == 13:
            print("Local: B6B")
            local = "B6B"
        elif posicao_aprovados[0] == 14:
            print("Local: B6C")
            local = "B6C"
        elif posicao_aprovados[0] == 15:
            print("Local: B7A")
            local = "B7A"
        elif posicao_aprovados[0] == 16:
            print("Local: B7B")
            local = "B7B"
        elif posicao_aprovados[0] == 17:
            print("Local: B8A")
            local = "B8A"
        elif posicao_aprovados[0] == 18:
            print("Local: B8B")
            local = "B8B"
        elif posicao_aprovados[0] == 19:
            print("Local: B9A")
            local = "B9A"
        elif posicao_aprovados[0] == 20:
            print("Local: B9B")
            local = "B9B"
        elif posicao_aprovados[0] == 21:
            print("Local: B9C")
            local = "B9C"
        elif posicao_aprovados[0] == 22:
            print("Local: B10.1")
            local = "B10.1"
        elif posicao_aprovados[0] == 23:
            print("Local: B10.2")
            local = "B10.2"
        elif posicao_aprovados[0] == 24:
            print("Local: B10.3")
            local = "B10.3"
        elif posicao_aprovados[0] == 25:
            print("Local: B10.4")
            local = "B10.4"
        elif posicao_aprovados[0] == 26:
            print("Local: B10.5")
            local = "B10.5"
        elif posicao_aprovados[0] == 27:
            print("Local: B11A")
            local = "B11A"
        elif posicao_aprovados[0] == 28:
            print("Local: B11B")
            local = "B11B"
        elif posicao_aprovados[0] == 29:
            print("Local: B11C")
            local = "B11C"
        elif posicao_aprovados[0] == 30:
            print("Local: B12A")
            local = "B12A"
        elif posicao_aprovados[0] == 31:
            print("Local: B12B")
            local = "B12B"
        elif posicao_aprovados[0] == 32:
            print("Local: B12C")
            local = "B12C"
        elif posicao_aprovados[0] == 33:
            print("Local: WC-M")
            local = "WC-M"
        elif posicao_aprovados[0] == 34:
            print("Local: WC-F")
            local = "WC-F"
        elif posicao_aprovados[0] == 35:
            print("Local: C1")
            local = "C1"
        elif posicao_aprovados[0] == 36:
            print("Local: C2")
            local = "C2"
        elif posicao_aprovados[0] == 37:
            print("Local: C3")
            local = "C3"
        elif posicao_aprovados[0] == 38:
            print("Local: C4")
            local = "C4"
        elif posicao_aprovados[0] == 39:
            print("Local: C5")
            local = "C5"
        else:
            print("Local: Não encontrado!")
            local = "nao encontrado"
    x = {
        'Status': 'Success',
        "search" : search.tolist(),
        "locale" : local,
        "result" : here.tolist()
    }
    json.dumps(x)
    if x == None:
        return ""
    return x
