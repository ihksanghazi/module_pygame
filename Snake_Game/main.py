import pygame  # Import pustaka pygame untuk membuat game
import sys  # Import pustaka sys untuk mengelola sistem
import random  # Import pustaka random untuk menghasilkan angka acak
import time  # Import pustaka time untuk mengatur waktu dalam game

# Inisialisasi pygame
check_errors = pygame.init()

# Menentukan ukuran layar game
frame_size_x = 720
frame_size_y = 480

# Menentukan judul jendela game
pygame.display.set_caption('Snake Game')

# Membuat jendela game dengan ukuran yang sudah ditentukan
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Mengontrol kecepatan permainan
fps_controller = pygame.time.Clock()

# Menentukan arah awal pergerakan ular
direction = "RIGHT"
change_to = direction

# Inisialisasi skor
score = 0

# Posisi awal kepala ular
snake_pos = [100, 50]

# Badan awal ular terdiri dari 3 bagian
snake_body = [[100, 50], [90, 50], [80, 50]]

# Posisi awal apel secara acak
apple_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
apple_spawn = True

# Warna yang digunakan dalam permainan
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Fungsi untuk menampilkan layar game over
def game_over():
    my_font = pygame.font.SysFont('Arial', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (360, 120)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Loop utama permainan
while True:
    # Mengecek event yang terjadi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Jika pemain menutup jendela, keluar dari permainan
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Jika tombol ditekan, ubah arah ular
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Pastikan ular tidak bisa bergerak ke arah berlawanan langsung
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # Menggerakkan ular berdasarkan arah yang dipilih
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Membersihkan layar game
    game_window.fill(white)
    
    # Menambahkan posisi baru kepala ular
    snake_body.insert(0, list(snake_pos))
    
    # Jika ular memakan apel, skor bertambah, dan apel respawn
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        score += 1
        apple_spawn = False
    else:
        # Jika tidak memakan apel, hapus bagian ekor agar panjang tidak bertambah
        snake_body.pop()
    
    # Menggambar badan ular
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    # Jika apel dimakan, buat apel baru
    if not apple_spawn:
        apple_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    apple_spawn = True
    
    # Menggambar apel
    pygame.draw.rect(game_window, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))
    
    # Mengecek apakah ular menabrak dinding
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
    
    # Mengecek apakah ular menabrak tubuhnya sendiri
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    # Menampilkan skor di layar
    score_font = pygame.font.SysFont('Arial', 20)
    score_surface = score_font.render('Score : ' + str(score), True, black)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (72, 15)
    game_window.blit(score_surface, score_rect)
    
    # Memperbarui tampilan game
    pygame.display.update()
    
    # Mengatur kecepatan permainan
    fps_controller.tick(10)
