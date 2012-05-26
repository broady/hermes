import par_bridge

class ClModule():
  def __init__(self, printer):
    self.printer = printer

  def run(self):
    info = par_bridge.Run("cl_info.par")
    for cl in info['incoming']:
      if cl['attention'] == True:
        self.printer.Print(str(cl['cl']) + ': ' + cl['description'].split('\n')[0])

if __name__ == '__main__':
  module = ClModule(None)
  module.run()
