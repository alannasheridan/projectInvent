# import RPi.GPIO as GPIO
# import pygame
# import json
# import time
# import threading

# # Configuration
# PIN_SOUND_MAP = {
#     17: "click.mp3",
#     27: "chime.mp3"
# }

# def setup_gpio():
#     GPIO.setmode(GPIO.BCM)
#     for pin in PIN_SOUND_MAP:
#         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# def play_sound(filename):
#     pygame.mixer.music.load(f"sounds/{filename}")
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         time.sleep(0.1)

# def gpio_listener():
#     setup_gpio()
#     pygame.mixer.init()
#     last_state = {pin: GPIO.input(pin) for pin in PIN_SOUND_MAP}
#     while True:
#         for pin in PIN_SOUND_MAP:
#             current_state = GPIO.input(pin)
#             if current_state != last_state[pin] and current_state == GPIO.LOW:
#                 print(f"Pin {pin} triggered: Playing {PIN_SOUND_MAP[pin]}")
#                 play_sound(PIN_SOUND_MAP[pin])
#             last_state[pin] = current_state
#         time.sleep(0.05)

# def start_gpio_thread():
#     threading.Thread(target=gpio_listener, daemon=True).start()

import platform

def start_gpio_thread(play_callback):
    if platform.system() != "Linux":
        print("Skipping GPIO setup — not running on Raspberry Pi.")
        return

    try:
        import RPi.GPIO as GPIO
        import threading
        import time
    except ImportError:
        print("RPi.GPIO module not found — GPIO will not work.")
        return

    button_pins = {
        "button1": 17,
        "button2": 18,
        "button3": 27
    }

    def watch_gpio():
        GPIO.setmode(GPIO.BCM)
        for pin in button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            for button, pin in button_pins.items():
                if GPIO.input(pin) == GPIO.LOW:
                    print(f"{button} pressed")
                    play_callback(button)
                    time.sleep(0.5)
            time.sleep(0.1)

    thread = threading.Thread(target=watch_gpio)
    thread.daemon = True
    thread.start()