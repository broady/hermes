# Copyright James McGill, 2011
# Author: James McGill (jmcgill@plexer.net)

import shine
import unicodedata
import tasks_module
import oncall_module
import cl_module
import calendar_module

class Printer():
  def __init__(self, client):
    self.client = client

  def Feed(self, lines):
    input = shine.shine.FeedMessage()
    input.set_num_lines(lines)
    self.client.Feed(input)

  def PrintChar(self, char):
    input = shine.shine.CharacterMessage()
    input.set_letter(char)
    self.client.Print(input)

  def Print(self, msg):
    if not msg.__class__ == ''.__class__:
      msg = unicodedata.normalize('NFKD', msg).encode('ascii', 'ignore')
    input = shine.shine.TextMessage()
    for i in range(0, len(msg)):
      input.set_msg(i, msg[i])
    self.client.Println(input)

  def PrintHeading(self, msg):
    # Turn Bold on.
    self.WriteRawBytes([27, 69, 1])

    # Increase the font size.
    size = 25
    self.WriteRawBytes([29, 33, size, 10])

    # Center
    self.WriteRawBytes([0x1B, 0x61, 1])

    # Send the message.
    self.Print(msg)

    # Turn bold off
    self.WriteRawBytes([27, 69, 0])

    # Normal height
    self.WriteRawBytes([29, 33, 10, 10])

    # Left align
    self.WriteRawBytes([0x1B, 0x61, 0])

  def WriteRawByte(self, byte):
    input = shine.shine.RawMessage()
    input.set_byte(byte)
    self.client.WriteRaw(input)

  def WriteRawBytes(self, bytes):
    for byte in bytes:
      self.WriteRawByte(byte)

  def ConfigureFor5V(self):
    self.WriteRawBytes([27, 55, 7, 200, 10])

  def HorizontalLine(self):
    self.WriteRawBytes([18, 42, 5, 320 / 8]);
    for i in range(5 * 320 / 8):
      self.WriteRawByte(255)

  def SetLineHeight(self, height = 32):
    self.WriteRawBytes([27, 51, height])

def Underline(printer):
  # Center, Underline, Left align, with vertical spacing.
  printer.Print(" ")
  printer.WriteRawBytes([0x1B, 0x61, 1])
  printer.Print("___________________")
  printer.WriteRawBytes([0x1B, 0x61, 0])
  printer.Print(" ")

def main():
  client = shine.Shine(
      '/dev/ttyACM0',  # Serial port.
      9600,                    # Baud rate.
      'hermes.shn')            # Protocol file.

  printer = Printer(client)

  printer.ConfigureFor5V()

  #tasks = tasks_module.TasksModule(printer)
  #tasks.run()

  #Underline(printer)

  #oncall = oncall_module.OnCallModule(
  #    printer,
  #    ["maps-api", "places-api", "spatial-data-api", "geo-tracking-api"],
  #    "jmcgill")
  #oncall.run()

  #Underline(printer)

  #cl = cl_module.ClModule(printer)
  #cl.run()

  #Underline(printer)

  calendar = calendar_module.CalendarModule(printer)
  calendar.run()

if __name__ == '__main__':
  main()
