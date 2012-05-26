import par_bridge
import datetime

def Date(timestamp):
  if timestamp == None:
    return "Forever"
  else:
    date = datetime.datetime.fromtimestamp(timestamp)

  # Account for timezone
  date = date + datetime.timedelta(hours=0)
  return date.strftime("%H:%M:%S %a %d/%m")

class OnCallModule():
  def __init__(self, printer, rotations, user):
    self.printer = printer
    self.rotations_ = rotations
    self.user_ = user

  def run(self):
    info = par_bridge.Run("oncall_info.par", rotations=",".join(self.rotations_))
    for rotation in info:
      r = info[rotation]
      if r['people'][0] == self.user_:
        self.printer.Print(rotation + ': Primary until: ' + Date(r['until']))

      if r['people'][1] == self.user_:
        self.printer.Print(rotation + ': Secondary until: ' + Date(r['until']))

      if 'next' in r and r['next'] == self.user_:
        end_of_today = datetime.date.today() + datetime.timedelta(days = 1)
        until = datetime.date.fromtimestamp(r['until'])
        if until < end_of_today:
          self.printer.Print(rotation + ': Primary from: ' + Date(r['until']))

if __name__ == '__main__':
  module = OnCallModule(None, ["maps-api", "places-api"], "jmcgill")
  module.run()
