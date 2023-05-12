import struct
import socket
import re
import time 
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import logging

logger = logging.getLogger(__name__)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 14100  # The port used by the server
TEXTFLOW = 'pias_ipc_textflow#'

def message(message: str):
    data = message.encode()
    size = struct.pack('>L', len(data))
    return size[::-1] + data

@dataclass
class RecievedMessage:
    recieved_lines: List["RecievedMessage.RecievedLine"] = field(
        default_factory=list,
        metadata={"type": "Element"}
    )
    @dataclass
    class RecievedLine:
        size: int 
        data: str

@dataclass
class Cache:
    data_array: list	



class TranslateReply:
    def __init__(self, data: Cache) -> None:
        self.data = data.data_array
        self.message = RecievedMessage()
        
    def to_line(self):
        while len(self.data[0]) > 0:
            size = ord(self.data[0])
            line = "".join(self.data[4:size + 4]).strip()
            self.message.recieved_lines.append(RecievedMessage.RecievedLine(size=size, data=line))
            del self.data[0: size + 4]


    def find_value(self, _type:str):
        for line in self.message.recieved_lines:
            if f"<{_type}>" in line.data:
                value = re.search('>(.*)</', line.data)
                return float(value.group(1))

@dataclass
class RecievedMessage:
    recieved_lines: List["RecievedMessage.RecievedLine"] = field(
        default_factory=list,
        metadata={"type": "Element"}
    )
    @dataclass
    class RecievedLine:
        size: int 
        data: str


class Client:
    def __init__(self, logging: bool = False) -> None:
        """
        Arg:
            logging (bool): set logging.

        """
        self.cache_recieved_bytes = Cache(data_array=[])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if logging:
            logger.info(f"Socket connect to port: {PORT} on ip: {HOST}")

        self.prefix = TEXTFLOW + "init"
        self.suffix = TEXTFLOW + "endofmessage"
        self.kill = TEXTFLOW + "killserver"


    def server_check(self):
        try:
            self.sock.connect((HOST, PORT))
            sent = self.sock.send(message(self.prefix))
            if sent == 0:
                return False
            else:
                self.sock.close()
                return True
        except ConnectionRefusedError as e:
            if logger:
                logger.exception(f"{e}")
            return False

    def send_from_stream(self, data: str):
        """
        Sends data line by line. The end of the line is denoted by the Line Feed character, decimal 10 character \n.
        """
        line = ""
        self.sock.connect((HOST, PORT))
        self.sock.sendall(message(self.prefix))
        for char in data:
            line += char
            if char == chr(10):
                try:
                    self.sock.send(message(line[:-1]))
                except ConnectionResetError as e:
                    if logger:
                        logger.exception(f"{e}")
                    time.sleep(1)
                    continue
                line = ""
        self.sock.sendall(message(self.suffix))  
        self.recieve_message()
        self.sock.close()

    def recieve_message(self):
        while True:
            data = self.sock.recv(1)
            self.cache_recieved_bytes.data_array.append(data.decode())
            if not data:
                break

    def send_from_file(self, path_to_source: Path):
        
        self.sock.connect((HOST, PORT))
        with path_to_source.open('r') as file:
            self.sock.send(message(self.prefix))
            for line in file.readlines():
                try:
                    self.sock.send(message(line[:-1]))
                except ConnectionResetError as e:
                    print(e)
                    time.sleep(2)
                    continue
            self.sock.send(message(self.suffix))
            self.sock.close()

    def recv_timeout(self, timeout=2):
        #make socket non blocking
                
        #total data partwise in an array
        total_data=[];
        data='';
        
        #beginning time
        begin = time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
            
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout * 2:
                break
            
            #recv something
            try:
                data = self.socket.recv(8192)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin = time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
        self.sock.close()
        #join all parts to make final string
        return ''.join(total_data)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, address: str):
        self._host = address

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, server_port: int):
        self._port = server_port
