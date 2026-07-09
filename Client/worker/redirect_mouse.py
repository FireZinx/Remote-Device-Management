from infrastructure.network.constants import PacketType

import pyautogui
import time

class Mouse:
    def redirect(self):
        while not self.close_threads:
            if self.mouse_click is None:
                time.sleep(0.01)
                continue

            if self.mouse_click == PacketType.RMOUSEBUTTON:
                pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1])

            elif self.mouse_click == PacketType.LMOUSEBUTTON:
                pyautogui.click(self.mouse_pos[0], self.mouse_pos[1])

            self.mouse_click = None