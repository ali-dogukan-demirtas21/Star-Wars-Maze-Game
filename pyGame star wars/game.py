# game.py - Ana oyun dosyası
import random
import pygame
import sys
import os
from pygame.locals import *
from config import *
from characters import *
from map_loader import harita_yukle
from utils import *

class Game:
    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        
        self.harita_dosyasi = os.path.join(MAPS_DIRECTORY, DEFAULT_MAP)
        self.harita, self.dusman_bilgileri = harita_yukle(self.harita_dosyasi)
        
        
        print("Yüklenen düşman bilgileri:", self.dusman_bilgileri)
        
        
        self.running = True
        self.game_over = False
        self.victory = False
        self.selected_character = None
        self.enemies = []
        self.current_path = []
        
        
        self.load_images()
        
        
        self.load_sounds()

    
    def load_images(self):
        
        self.images = {}
        
        for char_name, image_file in CHARACTER_IMAGES.items():
            try:
                self.images[char_name] = load_image(image_file)
                
                self.images[char_name] = pygame.transform.scale(
                    self.images[char_name], 
                    (CELL_SIZE, CELL_SIZE)
                )
                print(f"Karakter görseli yüklendi: {char_name}")
            except Exception as e:
                print(f"Karakter görseli yüklenirken hata: {char_name} - {e}")
        
        
        self.heart_images = {}
        print("Kalp görselleri yükleniyor...")
        
        for heart_type, image_file in HEART_IMAGES.items():
            try:
                
                image_path = resource_path(image_file, IMAGES_DIRECTORY)
                print(f"Kalp dosya yolu: {image_path}")
                
                
                self.heart_images[heart_type] = load_image(image_file)
                
                
                self.heart_images[heart_type] = pygame.transform.scale(
                    self.heart_images[heart_type], 
                    (40, 40)  
                )
                print(f"Kalp görseli yüklendi: {heart_type} - {image_file}")
            except Exception as e:
                print(f"Kalp görseli yüklenirken hata: {heart_type} - {image_file} - {e}")

        
        print(f"Yüklenen kalp görselleri: {list(self.heart_images.keys())}")

    def load_sounds(self):
        
        self.sounds = {}
        self.sounds['capture'] = load_sound(CAPTURE_SOUND)
        self.sounds['victory'] = load_sound(VICTORY_SOUND)
        self.sounds['game_over'] = load_sound(GAME_OVER_SOUND)
        self.sounds['background'] = load_sound(BACKGROUND_MUSIC)
        
        
        if self.sounds['background']:
            self.sounds['background'].set_volume(MUSIC_VOLUME)
            self.sounds['background'].play(-1)  

    def new_game(self):
        
        self.initialize_characters()
        
        
        self.game_over = False
        self.victory = False
        self.current_path = []
        self.enemy_paths = []  
        
        
        self.run()
        
    
    def initialize_characters(self):
        
        player_loc = Lokasyon(PLAYER_START_POS[0], PLAYER_START_POS[1])
        
        
        if self.selected_character == "Luke Skywalker":
            self.player = LukeSkywalker(player_loc)
        else:  
            self.player = MasterYoda(player_loc)
        
        
        self.enemies = []
        
        
        kapi_listesi = list(DOORS.keys())
        
        
        dusman_tipleri = ["Stormtrooper", "Darth Vader", "Kylo Ren"]
        
        
        kullanilan_kapilar = []
        
        for dusman_ad in dusman_tipleri:
            
            kullanilabilir_kapilar = [k for k in kapi_listesi if k not in kullanilan_kapilar]
            
            
            if not kullanilabilir_kapilar:
                kullanilabilir_kapilar = kapi_listesi
            
            kapi = random.choice(kullanilabilir_kapilar)
            kullanilan_kapilar.append(kapi)
            
            
            kapi_x, kapi_y = DOORS[kapi]
            konum = Lokasyon(kapi_x, kapi_y)
            
            print(f"Düşman oluşturuluyor: {dusman_ad}, Kapı: {kapi}, Konum: ({kapi_x}, {kapi_y})")
            
            # Düşmanı oluştur
            if dusman_ad == "Darth Vader":
                self.enemies.append(DarthVader(konum))
            elif dusman_ad == "Kylo Ren":
                self.enemies.append(KyloRen(konum))
            elif dusman_ad == "Stormtrooper":
                self.enemies.append(Stormtrooper(konum))
        
        print(f"Toplam {len(self.enemies)} düşman oluşturuldu.")
        
        
        self.update_enemy_paths()
    
    
    def character_selection_screen(self):
        
        selecting = True
        
        
        bg_frames, bg_durations = load_gif("character_select_background.gif")
        
        if bg_frames:
            current_frame = 0
            frame_time = 0
        
        
        button_width = 300
        button_height = 80
        luke_button_x = SCREEN_WIDTH // 4 - button_width // 2
        luke_button_y = 300
        yoda_button_x = 3 * SCREEN_WIDTH // 4 - button_width // 2
        yoda_button_y = 300
        
        while selecting:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    
                    luke_rect = pygame.Rect(luke_button_x, luke_button_y, button_width, button_height)
                    yoda_rect = pygame.Rect(yoda_button_x, yoda_button_y, button_width, button_height)
                    
                    if luke_rect.collidepoint(mouse_pos):
                        print("Luke Skywalker seçildi!")
                        self.selected_character = "Luke Skywalker"
                        selecting = False
                    elif yoda_rect.collidepoint(mouse_pos):
                        print("Master Yoda seçildi!")
                        self.selected_character = "Master Yoda"
                        selecting = False
            
            
            self.screen.fill(BLACK)
            
            
            if bg_frames:
                
                frame = bg_frames[current_frame]
                
                
                scaled_frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(scaled_frame, (0, 0))
                
                
                frame_time += self.clock.get_time()
                
                
                if frame_time >= bg_durations[current_frame]:
                    frame_time = 0
                    current_frame = (current_frame + 1) % len(bg_frames)
            
            
            title_overlay = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
            title_overlay.fill((0, 0, 0, 180)) 
            self.screen.blit(title_overlay, (0, 50))
            
            
            draw_text(self.screen, "Star Wars Labyrinth", FONT_SIZE_LARGE, 
                    SCREEN_WIDTH // 2, 70, YELLOW)
            draw_text(self.screen, "Karakterinizi Seçin", FONT_SIZE_MEDIUM, 
                    SCREEN_WIDTH // 2, 130, WHITE)
            
            
            select_overlay = pygame.Surface((SCREEN_WIDTH, 400), pygame.SRCALPHA)
            select_overlay.fill((0, 0, 0, 150))  
            self.screen.blit(select_overlay, (0, 250))
            
            
            pygame.draw.rect(self.screen, BUTTON_INACTIVE_COLOR, 
                            pygame.Rect(luke_button_x, luke_button_y, button_width, button_height))
            pygame.draw.rect(self.screen, BLACK, 
                            pygame.Rect(luke_button_x, luke_button_y, button_width, button_height), 2)
            luke_text = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM).render("Luke Skywalker", True, BUTTON_TEXT_COLOR)
            luke_text_rect = luke_text.get_rect(center=(luke_button_x + button_width//2, luke_button_y + button_height//2))
            self.screen.blit(luke_text, luke_text_rect)
            
            
            if "Luke Skywalker" in self.images:
                luke_img = self.images["Luke Skywalker"]
                luke_img = pygame.transform.scale(luke_img, (200, 200))
                luke_img_rect = luke_img.get_rect()
                luke_img_rect.center = (SCREEN_WIDTH // 4, 500)
                self.screen.blit(luke_img, luke_img_rect)
            
            
            draw_text(self.screen, "3 canı vardır", FONT_SIZE_MEDIUM, 
                    SCREEN_WIDTH // 4, 650, WHITE)
            
            
            pygame.draw.rect(self.screen, BUTTON_INACTIVE_COLOR, 
                            pygame.Rect(yoda_button_x, yoda_button_y, button_width, button_height))
            pygame.draw.rect(self.screen, BLACK, 
                            pygame.Rect(yoda_button_x, yoda_button_y, button_width, button_height), 2)
            yoda_text = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM).render("Master Yoda", True, BUTTON_TEXT_COLOR)
            yoda_text_rect = yoda_text.get_rect(center=(yoda_button_x + button_width//2, yoda_button_y + button_height//2))
            self.screen.blit(yoda_text, yoda_text_rect)
            
            
            if "Master Yoda" in self.images:
                yoda_img = self.images["Master Yoda"]
                yoda_img = pygame.transform.scale(yoda_img, (200, 200))
                yoda_img_rect = yoda_img.get_rect()
                yoda_img_rect.center = (3 * SCREEN_WIDTH // 4, 500)
                self.screen.blit(yoda_img, yoda_img_rect)
            
            
            draw_text(self.screen, "Yakalandığında sadece 0.5 can kaybeder", FONT_SIZE_MEDIUM, 
                    3 * SCREEN_WIDTH // 4, 650, WHITE)
            
            pygame.display.flip()
    
    def run(self):
        
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                
                
                if not self.game_over and not self.victory:
                    self.move_player(event.key)
    
    def move_player(self, key):
        
        x, y = self.player.konum.getX(), self.player.konum.getY()
        new_x, new_y = x, y
        
        
        if key in MOVEMENT_KEYS["UP"]:
            new_y -= 1
        elif key in MOVEMENT_KEYS["DOWN"]:
            new_y += 1
        elif key in MOVEMENT_KEYS["LEFT"]:
            new_x -= 1
        elif key in MOVEMENT_KEYS["RIGHT"]:
            new_x += 1
        
        
        if self.is_valid_move(new_x, new_y):
            
            collision_detected = False
            for enemy in self.enemies:
                enemy_x, enemy_y = enemy.konum.getX(), enemy.konum.getY()
                if new_x == enemy_x and new_y == enemy_y:
                    
                    collision_detected = True
                    break
            
            
            self.player.konum.setX(new_x)
            self.player.konum.setY(new_y)
            
            
            if collision_detected:
                self.handle_capture()
                return  
            
            
            if not self.check_collision():  
                
                self.move_enemies()
                
                
                if (new_x, new_y) == GOAL_POS:
                    self.victory = True
                    if self.sounds['victory']:
                        self.sounds['victory'].play()

    def check_collision(self):
        """Oyuncu ve düşmanlar arasında çarpışma kontrolü yapar"""
        player_x, player_y = self.player.konum.getX(), self.player.konum.getY()
        
        for enemy in self.enemies:
            enemy_x, enemy_y = enemy.konum.getX(), enemy.konum.getY()
            
            
            if player_x == enemy_x and player_y == enemy_y:
                print(f"Çarpışma algılandı! Oyuncu: ({player_x}, {player_y}), Düşman: {enemy.getAd()}")
                self.handle_capture()
                return True  
        
        return False  


    def update_enemy_paths(self):
        """Düşman rotalarını günceller"""
        self.enemy_paths = []
        
        for enemy in self.enemies:
            
            path = enemy.EnKisaYol(self.harita, self.player.konum)
            
            self.enemy_paths.append(path)



    def is_valid_move(self, x, y):
        
        if not (0 <= x < len(self.harita[0]) and 0 <= y < len(self.harita)):
            return False
        
        
        return self.harita[y][x] == PATH
    
    def move_enemies(self):
        
        self.enemy_paths = []
        
        for enemy in self.enemies:
           
            path = enemy.EnKisaYol(self.harita, self.player.konum)
            
            
            self.enemy_paths.append(path)
            
            
            if path and len(path) > 1:
                
                if "Kylo Ren" in enemy.getAd() and len(path) > 2:
                    
                    next_pos = path[2]  
                else:
                    
                    next_pos = path[1]  
                    
                enemy.konum.setX(next_pos[0])
                enemy.konum.setY(next_pos[1])
        
        
        self.check_collision()
    
    def handle_capture(self):
        
        if self.sounds['capture']:
            self.sounds['capture'].play()
        
        
        self.player.yakalanma()
        
        
        if self.player.getCan() <= 0:
            self.game_over = True
            if self.sounds['game_over']:
                self.sounds['game_over'].play()
        else:
            
            self.reset_characters()

    def reset_characters(self):
        
        player_loc = Lokasyon(PLAYER_START_POS[0], PLAYER_START_POS[1])
        self.player.setKonum(player_loc)
        
        
        self.enemies.clear()
        
        
        self.enemy_paths = []
        self.current_path = []
        
        
        dusman_tipleri = ["Stormtrooper", "Darth Vader", "Kylo Ren"]
        kullanilan_kapilar = []
        kapi_listesi = list(DOORS.keys())
        
        print("------ Karakterler sıfırlanıyor ------")
        
        for dusman_ad in dusman_tipleri:
            
            kullanilabilir_kapilar = [k for k in kapi_listesi if k not in kullanilan_kapilar]
            if not kullanilabilir_kapilar:
                kullanilabilir_kapilar = kapi_listesi
            
            kapi = random.choice(kullanilabilir_kapilar)
            kullanilan_kapilar.append(kapi)
            
            
            kapi_x, kapi_y = DOORS[kapi]
            
            
            print(f"Düşman yeniden oluşturuluyor: {dusman_ad}, Kapı: {kapi}, Konum: ({kapi_x}, {kapi_y})")
            
            
            konum = Lokasyon(kapi_x, kapi_y)
            
            
            if dusman_ad == "Darth Vader":
                dsman = DarthVader(konum)
                self.enemies.append(dsman)
                print(f"Darth Vader'ın konumu: ({dsman.konum.getX()}, {dsman.konum.getY()})")
            elif dusman_ad == "Kylo Ren":
                dsman = KyloRen(konum)
                self.enemies.append(dsman)
                print(f"Kylo Ren'in konumu: ({dsman.konum.getX()}, {dsman.konum.getY()})")
            elif dusman_ad == "Stormtrooper":
                dsman = Stormtrooper(konum)
                self.enemies.append(dsman)
                print(f"Stormtrooper'ın konumu: ({dsman.konum.getX()}, {dsman.konum.getY()})")
        
        print(f"Toplam {len(self.enemies)} düşman yeniden oluşturuldu.")
        
        
        self.update_enemy_paths()
        
        
        for i, enemy in enumerate(self.enemies):
            print(f"Düşman {i+1}: {enemy.getAd()}, Konum: ({enemy.konum.getX()}, {enemy.konum.getY()})")
    
    def update(self):
        
        pass  
    
    
    def draw(self):
        
        self.screen.fill(BLACK)
        
        
        offset_x, offset_y = draw_grid(self.screen, self.harita)
        
        
        if hasattr(self, 'enemy_paths'):
            for i, path in enumerate(self.enemy_paths):
                if not path:
                    continue
                    
                
                if i < len(self.enemies):
                    enemy_name = self.enemies[i].getAd()
                    if "Darth Vader" in enemy_name:
                        path_color = (200, 0, 0)  
                    elif "Kylo Ren" in enemy_name:
                        path_color = (255, 80, 80)  
                    else:
                        path_color = (255, 0, 0)  
                else:
                    path_color = (255, 0, 0)  
                
                
                draw_path(self.screen, path, path_color, 2, offset_x, offset_y)
        
        
        player_x, player_y = self.player.konum.getX(), self.player.konum.getY()
        player_rect = pygame.Rect(
            offset_x + (player_x * CELL_SIZE), 
            offset_y + (player_y * CELL_SIZE), 
            CELL_SIZE, 
            CELL_SIZE
        )
        
        if self.player.getAd() in self.images:
            self.screen.blit(self.images[self.player.getAd()], player_rect)
        else:
            pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect)
        
        
        for enemy in self.enemies:
            enemy_x, enemy_y = enemy.konum.getX(), enemy.konum.getY()
            enemy_rect = pygame.Rect(
                offset_x + (enemy_x * CELL_SIZE), 
                offset_y + (enemy_y * CELL_SIZE), 
                CELL_SIZE, 
                CELL_SIZE
            )
            
            if enemy.getAd() in self.images:
                self.screen.blit(self.images[enemy.getAd()], enemy_rect)
            else:
                
                pygame.draw.rect(self.screen, ENEMY_COLOR, enemy_rect)
                
                text = pygame.font.SysFont(FONT_NAME, 12).render(enemy.getAd()[:4], True, WHITE)
                text_rect = text.get_rect(center=(
                    offset_x + (enemy_x * CELL_SIZE) + CELL_SIZE // 2, 
                    offset_y + (enemy_y * CELL_SIZE) + CELL_SIZE // 2
                ))
                self.screen.blit(text, text_rect)
        
        
        heart_spacing = CELL_SIZE  
        heart_y = offset_y  
        
        
        if self.player.getAd() == "Luke Skywalker":
            
            max_hearts = 3
            current_health = self.player.getCan()
            
            for i in range(max_hearts):
                heart_x = offset_x + (i * heart_spacing)  
                heart_rect = pygame.Rect(heart_x, heart_y, CELL_SIZE, CELL_SIZE)
                
                
                if hasattr(self, 'heart_images'):
                    if i < current_health and "full" in self.heart_images:
                        
                        heart_img = pygame.transform.scale(self.heart_images["full"], (CELL_SIZE, CELL_SIZE))
                        self.screen.blit(heart_img, heart_rect)
                    else:
                        
                        heart_img = pygame.transform.scale(self.heart_images["empty"], (CELL_SIZE, CELL_SIZE))
                        self.screen.blit(heart_img, heart_rect)
                else:
                    
                    color = RED if i < current_health else (100, 100, 100)
                    pygame.draw.rect(self.screen, color, heart_rect)
                    
        elif self.player.getAd() == "Master Yoda":
            
            max_hearts = 3
            current_health = self.player.getCan()
            
            for i in range(max_hearts):
                heart_x = offset_x + (i * heart_spacing)  
                heart_rect = pygame.Rect(heart_x, heart_y, CELL_SIZE, CELL_SIZE)
                
                
                if hasattr(self, 'heart_images'):
                    if i + 0.5 < current_health and "full" in self.heart_images:
                        
                        heart_img = pygame.transform.scale(self.heart_images["full"], (CELL_SIZE, CELL_SIZE))
                        self.screen.blit(heart_img, heart_rect)
                    elif i < current_health and "half" in self.heart_images:
                        
                        heart_img = pygame.transform.scale(self.heart_images["half"], (CELL_SIZE, CELL_SIZE))
                        self.screen.blit(heart_img, heart_rect)
                    else:
                       
                        heart_img = pygame.transform.scale(self.heart_images["empty"], (CELL_SIZE, CELL_SIZE))
                        self.screen.blit(heart_img, heart_rect)
                else:
                    
                    if i + 0.5 < current_health:
                        color = RED  
                    elif i < current_health:
                        color = (200, 100, 100)  
                    else:
                        color = (100, 100, 100)  
                    pygame.draw.rect(self.screen, color, heart_rect)
        
        
        char_text = f"Karakter: {self.player.getAd()}"
        draw_text(self.screen, char_text, FONT_SIZE_MEDIUM, SCREEN_WIDTH - 350, 20, WHITE)
        
        
        goal_rect = pygame.Rect(
            offset_x + (GOAL_POS[0] * CELL_SIZE), 
            offset_y + (GOAL_POS[1] * CELL_SIZE), 
            CELL_SIZE, 
            CELL_SIZE
        )
        if "Trophy" in self.images:
            self.screen.blit(self.images["Trophy"], goal_rect)
        
        
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_game_over(self):
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)  
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, "GAME OVER", FONT_SIZE_LARGE, 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED)
        draw_text(self.screen, "Tekrar oynamak için SPACE tuşuna basın", FONT_SIZE_MEDIUM, 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)
        
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.character_selection_screen()
            self.new_game()



    def draw_victory(self):
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)  
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, "TEBRİKLER!", FONT_SIZE_LARGE, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, GREEN)
        draw_text(self.screen, "Kupaya ulaştınız!", FONT_SIZE_MEDIUM, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        draw_text(self.screen, "Tekrar oynamak için SPACE tuşuna basın", FONT_SIZE_MEDIUM, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, WHITE)
        
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.character_selection_screen()
            self.new_game()
    
    
    def show_intro_screen(self):
        
        intro = True
        
        
        bg_frames, bg_durations = load_gif("intro_background.gif")  
        
        if bg_frames:
            current_frame = 0
            frame_time = 0
            
        while intro:
            self.clock.tick(FPS)
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        intro = False
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            
            self.screen.fill(BLACK)
            
            
            if bg_frames:
                
                frame = bg_frames[current_frame]
                
                
                scaled_frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(scaled_frame, (0, 0))
                
                
                frame_time += self.clock.get_time()
                
                
                if frame_time >= bg_durations[current_frame]:
                    frame_time = 0
                    current_frame = (current_frame + 1) % len(bg_frames)
            
            
            title_overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
            title_overlay.fill((0, 0, 0, 180))  
            self.screen.blit(title_overlay, (0, SCREEN_HEIGHT // 4 - 50))
            
            draw_text(self.screen, "STAR WARS LABİRENT", FONT_SIZE_LARGE, 
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, YELLOW)
            
            
            instr_overlay = pygame.Surface((SCREEN_WIDTH, 300), pygame.SRCALPHA)
            instr_overlay.fill((0, 0, 0, 150))  
            self.screen.blit(instr_overlay, (0, SCREEN_HEIGHT // 2 - 50))
            
            
            instructions = [
                "Labirentte dolaşarak kupaya ulaşmaya çalışın!",
                "Kötü karakterlerden kaçının.",
                "Klavye tuşlarını kullanarak hareket edin.",
                "İyi karakterinizi seçin ve maceranıza başlayın!",
                "",
                "Başlamak için ENTER tuşuna basın"
            ]
            
            for i, line in enumerate(instructions):
                draw_text(self.screen, line, FONT_SIZE_MEDIUM, 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40, WHITE)
            
            pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.show_intro_screen()
    game.character_selection_screen()
    game.new_game()
    pygame.quit()