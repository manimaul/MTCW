import Env
import shlex, subprocess

command = "rsync -avz --include \"*.kap\" --exclude \"*\" rsync://opencpn.xtr.cz/nga-kaps/ %s" %(Env.ngaBsbDir)
subprocess.Popen(shlex.split(command))