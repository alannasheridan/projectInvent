import RPi.GPIO as GPIO
import pygame
import json
import time
import threading

# Configuration
PIN_SOUND_MAP = {
    17: "click.mp3",
    27: "chime.mp3"
}

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in PIN_SOUND_MAP:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def play_sound(filename):
    pygame.mixer.music.load(f"sounds/{filename}")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def gpio_listener():
    setup_gpio()
    pygame.mixer.init()
    last_state = {pin: GPIO.input(pin) for pin in PIN_SOUND_MAP}
    while True:
        for pin in PIN_SOUND_MAP:
            current_state = GPIO.input(pin)
            if current_state != last_state[pin] and current_state == GPIO.LOW:
                print(f"Pin {pin} triggered: Playing {PIN_SOUND_MAP[pin]}")
                play_sound(PIN_SOUND_MAP[pin])
            last_state[pin] = current_state
        time.sleep(0.05)

def start_gpio_thread():
    threading.Thread(target=gpio_listener, daemon=True).start()
