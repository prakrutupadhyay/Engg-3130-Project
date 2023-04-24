
# To run this project, follow the steps shown below:

##clone the repo
1. gh repo clone prakrutupadhyay/Engg-3130-Project

##go into the cloned directory
2. cd ENGG-3130-Project


## install dependencies

3. pip install -r requirements.txt

# open jupyter notebook named "demo"

4. Run the first cell of the notebook

The project would be executed with all the modifications that we made.

##If you get the following error:

Traceback (most recent call last):
  File "C:\Users\PrakrutUpadhyay\Downloads\Engg-3130-Project\run.py", line 3, in <module>
    server.launch()
  File "C:\Users\PrakrutUpadhyay\anaconda3\lib\site-packages\mesa\visualization\ModularVisualization.py", line 403, in launch
    self.listen(self.port)
  File "C:\Users\PrakrutUpadhyay\anaconda3\lib\site-packages\tornado\web.py", line 2109, in listen
    server.listen(port, address)
  File "C:\Users\PrakrutUpadhyay\anaconda3\lib\site-packages\tornado\tcpserver.py", line 151, in listen
    sockets = bind_sockets(port, address=address)
  File "C:\Users\PrakrutUpadhyay\anaconda3\lib\site-packages\tornado\netutil.py", line 161, in bind_sockets
    sock.bind(sockaddr)
OSError: [WinError 10048] Only one usage of each socket address (protocol/network address/port) is normally permitted


Answer: 1. Get the PID process using the command: Get-Process -Id (Get-NetTCPConnection -LocalPort 8521).OwningProcess
        2. Kill the Process: taskkill /F /PID <PID-num>
  
  This will resolve the issue
  
  

