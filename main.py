import pyautogui
import pygetwindow as gw
import time
from PIL import ImageGrab
import cv2
import tensorflow as tf
import numpy as np

class FNAFAutomation:
    def __init__(self, window_title):
        self.window = gw.getWindowsWithTitle(window_title)[0]  
        self.current_x = 0
        self.current_y = 0

        self.left_light = False
        self.left_door = False
        self.right_light = False
        self.right_door = False

        self.chica_state = False
        self.bonnie_state = False
        self.freddy_state = False
        self.foxy_state = False

        self.chica_present = False
        self.bonnie_present = False
        self.foxy_check = 0
        self.foxy_check_num = 20

        self.right_camera_state = 'chica'
        self.chica_checks = 2

        self.bonnie_last_visit = 0
        self.foxy_last_visit = time.time()

        self.pre_screen = None

        self.foxy_model = tf.keras.models.load_model('foxy_detector.h5')
        self.freddy_model = tf.keras.models.load_model('freddy_detector.h5')

        self.mode = 0
        self.start = time.time()
        self.loop_start = time.time()

    def fail_safe(self):
        print(f"{int((time.time() - self.start) / 89)}:{int((60 / 89) * ((time.time() - self.start) % 89))}")
        if (pyautogui.position() == (0,0)):
            raise Exception('Exiting due to mouse position') 

    def move_to_relative_position(self, x, y, duration=0, click=False):
        # Calculate the relative position based on window dimensions
        self.current_x = self.window.left + int(self.window.width * x * 0.995)
        self.current_y = self.window.top + int(self.window.height * y * 0.995)
        pyautogui.moveTo(self.current_x, self.current_y, duration=duration)
        if click:
            pyautogui.click()

    def color_match(self, color, tolerance=10):
        # Get the pixel color at the specified position
        pixel_color = pyautogui.pixel(pyautogui.position()[0], pyautogui.position()[1])
        
        # Check if the pixel color matches the specified color within the tolerance
        for i in range(3):
            if abs(pixel_color[i] - color[i]) > tolerance:
                return False
        return True

    def press_button(self, side, button, on):
        # Move to the button position and press it
        if side == 'left':
            if button == 'light':
                if self.left_light == on:
                    return
                
                if on:
                    self.right_light = False

                self.left_light = on

                on_color = (100, 100, 100)
                off_color = (199, 202, 213)
                self.move_to_relative_position(0.05, 0.63)
            else:
                if self.bonnie_present and not on:
                    return
                
                if self.left_door == on:
                    return
                self.left_door = on
                on_color = (178, 0, 0)
                off_color = (90, 204, 0)
                self.move_to_relative_position(0.05, 0.47)    
        else:
            if button == 'light':                
                if self.right_light == on:
                    return
                
                if on:
                    self.left_light = False

                self.right_light = on
                on_color = (86, 86, 86)
                off_color = (165, 172, 203)
                self.move_to_relative_position(0.95, 0.63)
            else:
                if (self.chica_present and not on) or (self.right_door == on):
                    return
                self.right_door = on
                on_color = (145, 0, 0)
                off_color = (50, 144, 0)
                self.move_to_relative_position(0.95, 0.47)

        while (True):
            self.fail_safe()

            # print(pyautogui.pixel(pyautogui.position()[0], pyautogui.position()[1]))

            on_color_match = self.color_match(on_color)
            off_color_match = self.color_match(off_color)

            if (on_color_match and not on
                or off_color_match and on):
                return
            
            if (off_color_match and not on
                or on_color_match and on):
                pyautogui.click()
                return

    def start_game(self, set_levels):
        # Start the game
        self.move_to_relative_position(0.21, 0.9, 0, True)

        time.sleep(0.7)

        if set_levels:

            for i in range(20):
                self.move_to_relative_position(0.24, 0.67 + (i % 3) * 0.01, 0, True)

            for i in range(20):
                self.move_to_relative_position(0.45, 0.67 + (i % 3) * 0.01, 0, True)

            for i in range(20):
                self.move_to_relative_position(0.67, 0.67 + (i % 3) * 0.01, 0, True)

            for i in range(20):
                self.move_to_relative_position(0.89, 0.67 + (i % 3) * 0.01, 0, True)

        time.sleep(0.5)
        self.move_to_relative_position(0.89, 0.9)
        pyautogui.click()
        time.sleep(8)

        self.start = time.time()

    def flick_camera(self):
        self.move_to_relative_position(0.5, 0.8)
        self.move_to_relative_position(0.5, 0.95)
        self.move_to_relative_position(0.5, 0.8)
    
    def use_freddy_model(self, check_num):
        time.sleep(0.2)
        left, top, right, bottom = self.window.left, self.window.top, self.window.right, self.window.bottom
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        frame = np.array(screenshot)

        # Convert RGB to BGR (OpenCV format)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        frame = cv2.resize(frame_bgr, (64, 64))  # Resize to the input size of the model
        frame = frame / 255.0  # Normalize to [0,1]
        frame = np.expand_dims(frame, axis=0)  # Add batch dimension
        predictions = self.freddy_model.predict(frame)

        predicted_class_index = np.argmax(predictions[0])

        if (predicted_class_index == 0):
            self.chica_checks = 2
            print('Predicted: Chica')

        if (predicted_class_index == 1):
            print('Predicted: None')

            if (check_num == 0 and self.foxy_check > 0):
                self.foxy_check = 1000


        if (predicted_class_index == 2):
            print('Predicted: Freddy')

    def cycle(self):
        self.fail_safe()

        if (time.time() - self.loop_start < 30):
            self.mode = 0
        elif (time.time() - self.loop_start < 5 * 90 + 35):
            self.mode = 1
        elif (time.time() - self.loop_start < 6 * 90 + 60):
            self.mode = 2
        else:
            self.mode = 3

        if (self.mode == 0):
            if (not self.bonnie_present and not self.chica_present):
                time.sleep(0.35)

            # Check Freddy
            self.flick_camera()
            self.move_to_relative_position(0.85, 0.87, 0.15, True)

            print('Checking Freddy')

            self.use_freddy_model(0)

            self.flick_camera()
            self.press_button('right', 'door', False)

        if (self.mode == 1):
            if (not self.bonnie_present and not self.chica_present):
                time.sleep(0.3)

            # Check Bonnie
            if time.time() - self.bonnie_last_visit >= 10:
                self.press_button('left', 'light', True)

                self.move_to_relative_position(0.35, 0.43)
                time.sleep(0.1)

                bonnie_detected = True
                for _ in range(3):
                    if self.color_match((16, 23, 36)):
                        bonnie_detected = False
                        break

                
                if (self.bonnie_present and not bonnie_detected):
                    self.bonnie_last_visit = time.time()

                self.bonnie_present = bonnie_detected

                time.sleep(0.12)
                self.press_button('left', 'door', bonnie_detected)
                self.press_button('left', 'light', False)

            # Check Freddy
            self.flick_camera()
            self.move_to_relative_position(0.85, 0.87, 0.1, True)

            print('Checking Freddy')

            self.use_freddy_model(0)

            self.flick_camera()
            self.press_button('right', 'door', False)


            # Check Chica
            if (self.chica_checks > 0):
                self.chica_checks -= 1

                self.press_button('right', 'light', True)

                self.move_to_relative_position(0.69, 0.61)
                time.sleep(0.08)

                chica_detected = False
                for _ in range(8):
                    if self.color_match((77, 89, 127)):
                        chica_detected = True
                        break


                if (chica_detected):
                    self.chica_checks = 1

                self.chica_present = chica_detected

                time.sleep(0.12)
                self.press_button('right', 'door', chica_detected)
                self.press_button('right', 'light', False)

        if (self.mode == 2):
            self.bonnie_present = False
            self.chica_present = False

            self.press_button('left', 'door', True)
            self.press_button('right', 'door', False)

        if (self.mode == 3):
            return False 

        return True
        
if __name__ == '__main__':
    while True:
        fnaf_bot = FNAFAutomation('Five Nights at Freddy\'s')

        fnaf_bot.start_game(True)

        main_loop = True

        while main_loop:
            fnaf_bot.fail_safe()
            main_loop = fnaf_bot.cycle()
        
