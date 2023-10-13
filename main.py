from process import Process
from alive import Alive
from election import Election
proc = Process()

proc.print_proc_info()
# proc.receive()

proc = Process()
alive = Alive()
election = Election()

proc.start()
alive.start()
election.start()