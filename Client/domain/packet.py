class PacketType():
    CAMERA_STREAM = b'\x01'
    CAMERA_ENABLE = b'\x02'
    SCREEN_STREAM = b'\x03'
    COMMAND_PACKET = b'\x04'
    MOUSE_PACKET = b'\x05'
    RMOUSEBUTTON = b'\x06'
    LMOUSEBUTTON = b'\x07'
    RESET = b'\x08'