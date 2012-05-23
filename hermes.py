# Copyright James McGill, 2011
# Author: James McGill (jmcgill@plexer.net)

import shine

def feed(client, lines):
  input = shine.shine.FeedMessage()
  input.set_num_lines(lines)
  client.Feed(input)

def prnt(client, letter):
  input = shine.shine.CharacterMessage()
  input.set_letter(letter)
  client.Print(input)

def println(client, msg):
  input = shine.shine.TextMessage()
  for i in range(0, len(msg)):
    input.set_msg(i, msg[i])
  client.Println(input)

def write_raw(client, byte):
  input = shine.shine.RawMessage()
  input.set_byte(byte)
  client.WriteRaw(input)

def main():
  client = shine.Shine(
      '/dev/tty.usbmodem621',  # Serial port.
      9600,                    # Baud rate.
      'hermes.shn')            # Protocol file.

  write_raw(client, 18)
  write_raw(client, 42)
  write_raw(client, 160)
  write_raw(client, 20)
  
  for i in range(0, 160 * 20):
    write_raw(client, 255);

  while 1:
    input_ = raw_input("Enter something: ")
    println(client, input_)

if __name__ == '__main__':
  main()

