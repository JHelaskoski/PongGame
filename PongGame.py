import pygame
import random

pygame.init()
naytto = pygame.display.set_mode((640, 480))
tausta = pygame.image.load("tausta.png")
tausta = pygame.transform.scale(tausta, (640, 480))

robo1 = pygame.image.load("ringo.png")
robo1 = pygame.transform.scale(robo1, (105, 105))

robo2 = pygame.image.load("nalle.png")
robo2 = pygame.transform.scale(robo2, (105, 105))

pallo = pygame.image.load("keksi.png")
pallo = pygame.transform.scale(pallo, (90, 90))


y1 = 240  # Robo1:n aloituspaikka
y2 = 240  # Robo2:n aloituspaikka
nopeus1 = 5
x2 = 640 - robo2.get_width()
pallo_x = 320  
pallo_y = 240
pallo_nopeus_x = 5 
pallo_nopeus_y = 3  

pisteet1 = 0 
pisteet2 = 0

kello = pygame.time.Clock()

# --- ALKUVALIKKO ---
valikko = True
while valikko:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_SPACE: 
                valikko = False

    naytto.blit(tausta, (0, 0))

    fontti = pygame.font.SysFont(None, 60)
    otsikko = fontti.render("PONG GAME", True, (181, 101, 29))
    naytto.blit(otsikko, (200, 100))

    fontti2 = pygame.font.SysFont(None, 40)
    ohje1 = fontti2.render("Pelaaja 1: W / S", True, (0, 0, 0,))
    ohje2 = fontti2.render("Pelaaja 2: Arrow keys", True, (0, 0, 0,) )
    ohje3 = fontti2.render("Press SPACE to start", True, (0, 0, 0,))

    naytto.blit(ohje1, (200, 200))
    naytto.blit(ohje2, (200, 250))
    naytto.blit(ohje3, (200, 330))

    pygame.display.flip()
    kello.tick(60)

# --- Pelin pyöritys ---

while True:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

    if pisteet1 == 5 or pisteet2 == 5:
        if pisteet1 == 5:
            voittaja_kuva = robo1
            voittaja_teksti = "Player 1. won!"
        else:
            voittaja_kuva = robo2 
            voittaja_teksti = "Player 2. won!"

        voitto_tausta = pygame.image.load("tausta.png")
        voitto_tausta = pygame.transform.scale(voitto_tausta, (640, 480))

        naytto.blit(voitto_tausta, (0, 0))

        kuva_x = 320 - voittaja_kuva.get_width() // 2
        kuva_y = 200 - voittaja_kuva.get_height() // 2
        naytto.blit(voittaja_kuva, (kuva_x, kuva_y))

        fontti = pygame.font.SysFont(None, 55)
        teksti = fontti.render(voittaja_teksti, True, (181, 101, 29))
        teksti_x = 320 - teksti.get_width() // 2
        teksti_y = 350
        naytto.blit(teksti, (teksti_x, teksti_y))

        fontti2 = pygame.font.SysFont(None, 45)
        ohje = fontti2.render("R = Restart E = Exit", True, (255, 255, 255))
        naytto.blit(ohje, (160, 420))

        pygame.display.flip()

        valinta_tehty = False
        while not valinta_tehty:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit() 
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_r: 
                        pisteet1 = 0 
                        pisteet2 = 0 
                        pallo_x, pallo_y = 320, 240 
                        y1, y2 = 240, 240 
                        valinta_tehty = True 
                    if tapahtuma.key == pygame.K_e: 
                        exit()

    painetut_napit = pygame.key.get_pressed()
    
    # Robo1 (w/s)
    if painetut_napit[pygame.K_w] and y1 > 0:
        y1 -= nopeus1 
    if painetut_napit[pygame.K_s] and y1 + robo1.get_height() < 480:
            y1 += nopeus1

    # Robo2 (nuolinäppäimillä)
    if painetut_napit[pygame.K_UP] and y2 > 0:
        y2 -= nopeus1 
    if painetut_napit[pygame.K_DOWN] and y2 + robo2.get_height() < 480:
        y2 += nopeus1

    pallo_x += pallo_nopeus_x
    pallo_y += pallo_nopeus_y

    # pallon osuminen ylä- ja alareunoihin
    if pallo_y <= 0 or pallo_y + pallo.get_height() >= 480:
        pallo_nopeus_y = -pallo_nopeus_y

    # Pallo osuu vasempaan pelaajaan
    if (pallo_x <= robo1.get_width() and pallo_y + pallo.get_height() >= y1 and pallo_y <= y1 + robo1.get_height()):
        pallo_nopeus_x = abs(pallo_nopeus_x)

    # Pallo osuu oikeaan pelaajaan
    if (pallo_x + pallo.get_width() >= x2 and pallo_y + pallo.get_height() >= y2 and pallo_y <= y2 + robo2.get_height()):
        pallo_nopeus_x = -abs(pallo_nopeus_x)

    # Pallo yli reunojen.
    if pallo_x < 0:
        pisteet2 += 1
        pallo_x, pallo_y = 320, 240
        pallo_nopeus_x = random.choice([-5, 5])
        pallo_nopeus_y = random.choice([-3, 3])

    if pallo_x > 640:
        pisteet1 += 1
        pallo_x, pallo_y = 320, 240
        pallo_nopeus_x = random.choice([-5, 5])
        pallo_nopeus_y = random.choice([-3, 3])

    naytto.blit(tausta, (0, 0))
    naytto.blit(robo1, (0, y1))
    naytto.blit(robo2, (x2, y2))
    naytto.blit(pallo, (pallo_x, pallo_y))

    # Pisteet
    fontti = pygame.font.SysFont(None, 55)
    teksti = fontti.render(f"{pisteet1} - {pisteet2}", True, (255, 255, 255))
    naytto.blit(teksti, (280, 20))

    pygame.display.flip()
    kello.tick(60)


