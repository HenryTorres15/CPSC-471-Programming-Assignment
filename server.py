# Server code
from s o c k e t import ∗

# The port on which to listen
serverPo rt = 12000

# Create a TCP socke t
s e r v e r So c k e t = s o c k e t (AF INET,SOCK STREAM) 9
# Bind the socke t to the port
se rv e rSo ck et . bind (( ’ ’ , serv erPo rt )) 12
# Start listening for incoming con necti on s
se rv erSo cke t . l ist e n (1)

print ”The s e r v e r i s ready to r e c e i v e ”

# The b u ffe r to s tore the received data
data = ””

# Forever a c c ep t incoming con ne ction s
while 1 :
# Accept a connection ; get client ’ s soc ke t

connection Socket , addr = serv erSocket . accept () 25
# Receive whatever the newly connected client has to send
data = con nectio n Socket . recv ( 40) 28
print data

# Close the so cke t
conn ection Socket . close ()