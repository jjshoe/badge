# Badger

This repository contains code (main.py) that works with a pimoroni badger 2040.

To load the code the simplest way is to use Thonny (https://thonny.org/). You can drag, drop, and execute code very easily. After installing thonny go to `Tools` -> `Options`. In the resulting popup select the `Interpreter` tab. In the drop down labeled `Which kind of interpreter should Thonny use for running your code?` make sure `MicroPython (Raspberry Pi Pico)` is selected. The option `Interrupt working program on connect` should be checked.  Also make sure your badger is selected from the "Port" drop down.

After loading the code on your device, you need to also load up configuration files. Each button corresponds to a specific named file such as:
* a.txt
* b.txt
* c.txt
* up.txt
* down.txt

The first line in the file should be set to the string you want to see at the top of the badge.
The second string of the file should be set to your name, the largest text to be displayed on screen.
The third line displays right below your name, it's the first of the bottom two rows.
The fourth line displays below your name, it's the second of the bottom two rows.
The fifth line can be anything you want coded into the QR code displayed to the right of your name and the bottom rows.

```
+-------------------------------+
| first line                    |
+-------------------------------+
|                     |         |
|     third line      | QR Code |
|                     |         |
+---------------------|         |
| fourth line         |         |
+---------------------+         |
| fifth line          |         |
+---------------------+---------+
```

While plugged into usb you can press any of the buttons to easily switch between config files.

The code in this repository is heavily modified from the following two sources:
* https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/badger2040/badge.py
* https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/badger2040/qrgen.py
