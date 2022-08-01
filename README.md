# **Team Two UAS-SAR Code Instructions**
Written by Team 2

# **Configuration Files**
**Configuration Files are a json File containing a dictionary of information that is crucial to both Receive and Analyze Data**
## Configuration Files - Emulator Type
**Emulator Type Config Files are used when running the emulator to receive data, and thus contain more information on the emulator configuration. Make sure that both emulator.py and analyzer.py refer to the same file. Below is a short description of values to be stored and modified in the file.**
1.   **Scan Start and Scan End** - Defines the Emulator Configuration Scan Start and End. These values help set the scope of the general range of the scan. See MRM API for more information. Scan Start should usually start at 0. 
2. **Base Integration Index** - Defines the Emulator Configuration Base Integration Index. See MRM API for more information.
3. **X and Y Values** - Defines the size of the image created. The image will be set to X meters by Y meters, where (0, 0) is the bottom left corner. The larger the X and Y values are, the more "zoomed out" the image will be.
4. **X_RES and Y_RES Values** - Defines the shift of the Axis in the image. The X_RES value will shift the X-Axis by X_RES meters to the left. The Y_RES value will shift the Y-Axis X_RES meters down. These values help focus on the image. 
5. **Scan Amount**  - Defines the number of Scans that the emulator will do. See MRM API for more information.
6. **Skip** - Defines the number of scans that will be skipped over. 
7. **Contrast Value** - Increasing this value increases the contrast by taking all of the amplitudes in the pixel and raising it to the Contrast Value. A Contrast Value of 1 is the default Contrast. 
8. **Transmit Gain** - Defines the Emulator Configuration Transmit Gain. See MRM API for more information. Default value is 63. 
9. **Scan Interval** - Defines the Emulator Configuration Scan Interal. See MRM API for more information. 

## Configuration Files - Analyzer Type
**Analyer Type Config Files are used when directly running the Analyzer.py. Has less information compared to Emulator Type Config Files. Below is a short description of values to be stored and modified in the file.**
1. **X and Y Values** - Defines the size of the image created. The image will be set to X meters by Y meters, where (0, 0) is the bottom left corner. The larger the X and Y values are, the more "zoomed out" the image will be.
2. **X_RES and Y_RES Values** - Defines the shift of the Axis in the image. The X_RES value will shift the X-Axis by X_RES meters to the left. The Y_RES value will shift the Y-Axis X_RES meters down. These values help focus on the image. 
3. **Skip** - Defines the number of scans that will be skipped over. 
4. **Contrast Value** - Increasing this value increases the contrast by taking all of the amplitudes in the pixel and raising it to the Contrast Value. A Contrast Value of 1 is the default Contrast. 
























# team2
Team 2 💪

Sign in sheet:  
Ty  
Tanush  
Jessica  
Ellie  
Felix  
