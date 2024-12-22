from CovertChannelBase import CovertChannelBase
import scapy.all as scapy
import time

class MyCovertChannel(CovertChannelBase):
    
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        self.array = []
        """
        - You can edit __init__.
        """
        pass
    def send(self, log_file_name):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name,min_length=16,max_length=16)
        index = 0
        flag = True
        while True:
            for i in range(0,2):
                message = binary_message[index + i*4 :index + i*4 +4]
                random_delay = self.generate_random_binary_message(min_length=2,max_length=2)
                delay = int(random_delay,2)
                sum0 = int(message[0]) + int(message[1]) + int(message[2]) + int(message[3])
                sum1 = int(message[1]) + int(message[2]) + int(message[3])
                sum2 = int(message[2]) + int(message[3])
                sum3 = int(message[3])
                sum0 = bin(sum0)
                sum1 = bin(sum1)
                sum2 = bin(sum2)
                sum3 = bin(sum3)
                sum0 = sum0[2:]
                sum1 = sum1[2:]
                sum2 = sum2[2:]
                sum3 = sum3[2:]
                sum0 = (4 - len(sum0))* "0" + sum0
                sum1 = (4 - len(sum1))* "0" + sum1
                sum2 = (4 - len(sum2))* "0" + sum2
                sum3 = (4 - len(sum3))* "0" + sum3
                last_16 = sum3[0:2] + sum2[0:2] + sum0[0:2] + sum1[0:2] + sum0[2:] + sum1[2:] + sum3[2:] + sum2[2:]
                disp = int(last_16,2)
                disp = disp ^ delay
                packet = scapy.IP(dst = "receiver")/scapy.UDP() / scapy.NTP(delay = delay,dispersion = disp)
                if flag:
                    t0 = time.time()
                    flag = False
                CovertChannelBase.send(self,packet)
            if binary_message[index:index+8] == "00101110":
                t1 = time.time()
                break
            index = index +8
        
        print(t1-t0)
        
        
            
    def stop_func(self,packet):
        if(len(self.array) < 2):
            return False
        if(int(self.array[-1][scapy.NTP].dispersion) ^ int(self.array[-1][scapy.NTP].delay) == 225 and int(self.array[-2][scapy.NTP].dispersion) ^ int(self.array[-2][scapy.NTP].delay) == 81):
            return True
        return False
    
    def receive(self,  log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        
        
        scapy.sniff(stop_filter = self.stop_func,filter = "host sender and port ntp" ,prn = lambda x: self.array.append(x))
        buffer = ""
        for i in self.array:
            disp = int(i[scapy.NTP].dispersion)
            delay = int(i[scapy.NTP].delay)
            disp = disp ^ delay
            disp = bin(disp)
            disp = disp[2:]
            disp = (16 - len(disp))* "0" + disp
            sum0 = disp[4:6] + disp[8:10] 
            sum1 = disp[6:8] + disp[10:12] 
            sum2 = disp[2:4] + disp[14:16] 
            sum3 = disp[0:2] + disp[12:14]
            if(sum0 == sum1):
                buffer = buffer + "0"
            else:
                buffer = buffer + "1"
            if(sum1 == sum2):
                buffer = buffer + "0"
            else:
                buffer = buffer + "1"
            if(sum2 == sum3):
                buffer = buffer + "0"
            else:
                buffer = buffer + "1"
            if(int(sum3,2) == 0):
                buffer = buffer + "0"
            else:
                buffer = buffer + "1"
        i = 0
        buffer2 = ""
        while i < len(buffer):
            buffer2 = buffer2 + self.convert_eight_bits_to_character(buffer[i:i+8])
            i = i + 8
        self.log_message(buffer2, log_file_name)
            
                   
        
        
        
