#include <shine.h>

#include <SoftwareSerial.h>
#include <Thermal.h>

// Include the code generated from the protocol file.
#include "hermes.shn.h"

int printer_RX_Pin = 2;
int printer_TX_Pin = 3;

Thermal printer(printer_RX_Pin, printer_TX_Pin, 19200);

void setup() {
  Shine.begin(9600);  
  // printer.setSize('S');
  // printer.setPrintDensity(50);
}

void loop() {
  Shine.loop();
}

void WriteRaw(RawMessage &input) {
  printer.write(input.get_byte());
}

void Print(CharacterMessage &input) {
  printer.print(char(input.get_letter()));
}

void Println(TextMessage &input) {
  int sz = input.msg_size();
  for (int i = 0; i < sz; ++i) {
    printer.print(char(input.get_msg(i)));
  }
  printer.feed();
}

void Feed(FeedMessage &input) {
  for (int i = 0; i < input.get_num_lines(); ++i) {
    printer.feed();
  }
}

