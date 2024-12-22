# Covert Storage Channel that exploits Protocol Field Manipulation using Root Dispersion field in NTP

NTP protocol is used to synchronize entities to a single clock which is very important for the whole consistency of the systems and their interactions. NTP protocol has Root Dispersion field. This field indicates the error margin of the NTP server with respect to the master clock. In this study we are manipulating the Root Dispersion field of the NTP message to carry a covert message.

## Method
- First we are taking the message that we want to convey in ASCII format in which one character is encoded as 8 bits.
- Then, we are dividing the 8 bit character to 2 4-bit chunks, in which each message will transmit 1 4-bit chunk.
- The manipulated field (Root Dispersion) is 32 bits. First 16 bits gives dispersion in seconds. Last 16 bits gives the dispersion in miliseconds. We decided to utilize only the last 16 bits because a high dispersion in order of seconds may cause attention. Thus, we are setting the first 16 bits to zero and we are encoding our message only in the last 16 bits. 
### Sender Side
- In the sender side, we are going to encode each 4 bit chunk to 16-bit.
- For each chunk, we are calculating 4 different 4-bit sums by following the below equations:

    sum1 = sum of all 4 bits

    sum2 = sum of last 3 bits

    sum3 = sum of last 2 bits

    sum4 = last bit

- This sums are not 4-bit long but in order to normalize, we are adding most significant 0's to convert them to 4-bit long sums.
- We divide each sum into 2-bit chunks. First chunk includes most significant 2 bits. Second chunk includes least significant 2 bits. We will denote the first chunk as sumX/1, and the second chunk as sumX/2. At the end we have 8 2-bit chunks.
- We are shuffling these 2-bit chunks to create our 16-bit message by following the below technique:

    16-bit message = sum4/1 ++ sum3/1 ++ sum1/1 ++ sum2/1 ++ sum1/2 ++ sum2/2 ++ sum4/2 ++ sum3/2
- We intentionally put the first chunks which includes the most significant bits of the sums (which are mostly 0's) in most significant bits of the 16-bit message in order to make dispersion smaller which will not be suspicious.
- We are performing bitwise XOR on the created 16-bit value and the least significant 16 bits of the Root Delay for further encoding our message. (We are not manipulating the Root Delay, we are just using its value.)
- Then, we are sending the packet with Root dispersions least significant 16-bits equal to the our manipulated 16-bit message.
- We are sending each chunk in a loop to receiver, until there is a "." character which signals end of message.
### Receiver Side
- Upon receiving the NTP message, first we perform XOR again on Root Dispersion's least significant 16-bits with Root Delay's least significant 16-bits to recover the encoded message.
- Then, we are recovering the sums by reverting the process in the sender as explained below:

    sum1 = 16-bit message[4:6] + 16-bit message[8:10].

    sum2 = 16-bit message[6:8] + 16-bit message[10:12].

    sum3 = 16-bit message[2:4] + 16-bit message[14:16].

    sum4 = 16-bit message[0:2] + 16-bit message[12:14].

- Then, we are recovering our original 4-bit message by comparing sums:

    if sum1 == sum2:
        message[0] = 0; else: message[0] =1;

    if sum2 == sum3:
        message[1] = 0; else: message[1] =1;

    if sum3 == sum4:
        message[2] = 0; else: message[2] =1;

    message[3] = sum4;

- Then, for each 2 packets we obtain a ASCII character and we log it.
- We are iterating this procedure until we get a "." character indicating end of message.
## Channel Capacity
We calculated our time as 0.5470213890075684 seconds. We estimate our channel capacity as 128/0.5470213890075684 = 233.9945 bits per second.


