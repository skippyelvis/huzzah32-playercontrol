import wifi
import socketpool
import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

class Joywing:

  def __init__(self):
    self.right = const(6)
    self.down = const(7)
    self.left = const(9)
    self.up = const(10)
    self.sel = const(14)
    self.mask = const(
      (1 << self.right)
      | (1 << self.down)
      | (1 << self.left)
      | (1 << self.up)
      | (1 << self.sel)
    )
    i2c = board.I2C()
    self.ss = Seesaw(i2c)
    self.ss.pin_mode_bulk(self.mask, self.ss.INPUT_PULLUP)

  def which_button(self):
    buttons = self.ss.digital_read_bulk(self.mask)
    if not buttons & (1 << self.right):
      return "right"
    if not buttons & (1 << self.down):
      return "down"
    if not buttons & (1 << self.left):
      return "left"
    if not buttons & (1 << self.up):
      return "up"
    if not buttons & (1 << self.sel):
      return "sel"

class Server:

  def __init__(self, remote):
    self.ipv4s = {"oryxpro": "10.0.0.240"}
    self.remote = remote
    self.pool = socketpool.SocketPool(wifi.radio)
    self.joywing = Joywing()
    
  def build_message(self):
    return self.joywing.which_button()

  def poll_forever(self):
    while True:
      sock = self.pool.socket()
      addr = (self.ipv4s[self.remote], 5000)
      sock.connect(addr)
      msg = self.build_message()
      if msg is not None:
        sock.send(bytes(msg, "UTF-8"))
        print("SENT: ", msg)
      sock.close()
      time.sleep(0.1)

serv = Server("oryxpro")
serv.poll_forever()
