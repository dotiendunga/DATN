import pygame


def playsound(file_path):
    try:
        # Khởi tạo Pygame
        pygame.init()

        # Tạo một mixer
        pygame.mixer.init()

        # Load file âm thanh
        sound = pygame.mixer.Sound(file_path)

        # Phát lại âm thanh
        sound.play()

        # Đợi cho âm thanh kết thúc
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)
        # Đóng Pygame
       
        pygame.mixer.quit()
        pygame.quit()
    except Exception as e:
        print("Error:", e)