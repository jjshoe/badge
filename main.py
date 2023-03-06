import time
import badger2040
import badger_os
import qrcode

# ------------------------------
#      File Functions
# ------------------------------
def read_config(config_file):
    
    try:
        config = open(config_file, "r")
        
        title = config.readline()
        name = config.readline()
        detail1 = config.readline()
        detail2 = config.readline()
        qr_code_url = config.readline()
    
        return {'title': title, 'name': name, 'detail1': detail1, 'detail2': detail2, 'qr_code_url': qr_code_url}
    except OSError:
        return {'title': 'Open failed: ' + config_file, 'name': 'Error', 'detail1': '', 'detail2': '', 'qr_code_url': ''}
    

# ------------------------------
#      Drawing functions
# ------------------------------

# QR codes are square, in portrait mode we need to scale based on available height
def scale_qr_code(qr_height, title_offset):
    # Total available height to take up    
    available_space = badger2040.HEIGHT - title_offset

    # Figure out how many times bigger we can get
    scale_factor = int(available_space / qr_height)

    # Multiply our current size by the scale factor
    new_size = qr_height * scale_factor

    # Though we only take in height, a QR code is square, so return the new size for both
    return new_size, new_size, scale_factor
    
# Draw the QR code to the screen
def draw_qr_code(code, title_offset):
    qr_width, qr_height = code.get_size()
    qr_width, qr_height, scale_factor = scale_qr_code(qr_height, title_offset)
    
    display.pen(15)
    display.rectangle(badger2040.WIDTH - qr_width, title_offset, qr_height, qr_width)
    display.pen(0)
    
    for x in range(qr_width):
        for y in range(qr_height):
            if code.get_module(x, y):
                display.rectangle(badger2040.WIDTH - qr_width + x * scale_factor, title_offset + y * scale_factor, scale_factor, scale_factor)
                
    return qr_width, qr_height

# Draw the badge, including user text
def draw_badge(config):
    # Common distances
    left_padding = 5
    right_padding = 5
    name_padding = 10
    details_height = 20
    title_height = 23
    details_height = 20
    name_height = badger2040.HEIGHT - title_height - (details_height * 2) - 2
    title_text_size = 1
    details_text_size = 2
    
    display.pen(0)
    display.clear()

    # Draw QR code
    code = qrcode.QRCode()
    code.set_text(config['qr_code_url'])
    qr_width, qr_height = draw_qr_code(code, title_height)

    # Draw the title
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("sans")
    display.thickness(1)

    # Draw the title, padded from the left, and lined up vertically half way through the title box.
    display.text(config['title'], left_padding, (title_height // 2) + 1, title_text_size)
    
    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, title_height + 1, badger2040.WIDTH - qr_width - right_padding, name_height)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(4)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(config['name'], name_size)
        if name_length >= (badger2040.WIDTH - qr_width - name_padding - right_padding) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(config['name'], (badger2040.WIDTH - qr_width - right_padding - name_length) // 2, (name_height // 2) + title_height + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, badger2040.HEIGHT - details_height * 2, badger2040.WIDTH - qr_width - right_padding, details_height - 1)
    display.rectangle(1, badger2040.HEIGHT - details_height, badger2040.WIDTH - qr_width - right_padding, details_height - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("bitmap8")

    display.thickness(1)
    display.text(config['detail1'], left_padding, badger2040.HEIGHT - (details_height * 2 - 2), details_text_size)

    # Draw the second detail's title and text
    display.thickness(1)
    display.text(config['detail2'], left_padding, badger2040.HEIGHT - (details_height - 2), details_text_size)


# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

while True:
    config = {}
    
    if display.pressed(badger2040.BUTTON_A):
        config = read_config("a.txt")
    elif display.pressed(badger2040.BUTTON_B):
        config = read_config("b.txt")
    elif display.pressed(badger2040.BUTTON_C):
        config = read_config("c.txt")
    elif display.pressed(badger2040.BUTTON_UP):
        config = read_config("up.txt")
    elif display.pressed(badger2040.BUTTON_DOWN):
        config = read_config("down.txt")
    else:
        time.sleep(0.1)
        continue
    
    draw_badge(config)    
    display.update()
    display.halt()
