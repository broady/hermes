import subprocess
import json
import os

def Run(par, **kwargs):
  args = [os.path.join(os.getcwd(), par)]
  for arg in kwargs:
    args.append("--" + arg + "=" + kwargs[arg])

  z = subprocess.Popen(args, stdout=subprocess.PIPE)
  return json.loads(z.communicate()[0])

if __name__ == "__main__":
  x = Run("oncall_info.par", rotations="maps-api")
