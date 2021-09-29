### Simple python NTRIP client
This is alpha code for proof of concept only.

1. Call a stream from RTK2GO.
2. Divide the string into messages.
3. Forward the entire bytes steam (multiple messsage) to a serial port.

This now works for me with UBlox ZED-F9P, the same as STR2STR 
Use at your own risk!