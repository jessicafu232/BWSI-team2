# **Team Two UAS-SAR Code Instructions**
Written by Team 2

# **Overview**
There are 3 main parts to operating our system. The Analyzer.py file, the master.py file, and Configuration Files. The Analyzer.py file takes raw data and implements backprojection and plots an image. The master.py file comunicates with the Emulator to generate and store raw scan information into a numpy file to be analyzed by Analyzer.py. Configuration Files define parameters for image formation and emulator configuration. 

When running pickle files that directly store raw information. Define the pickle file, and run the Analyzer directly. When running the Emulator, first start the emulator (refer to the Emulator README) and then run master.py: This will automatically run and store raw scan data. 


# **The master file**
master.py stores raw scan information. When trying to receive information from the emulator, make sure to run the correct configuration file.






# **Configuration Files**
Configuration Files are a json File containing a dictionary of information that is crucial to both Receive and Analyze Data. When forming images, modify these values to increase contrast, refocus the image, or increase resolution.
## Configuration Files - Emulator Type
Emulator Type Config Files are used when running the emulator to receive data, and thus contain more information on the emulator configuration. Make sure that both emulator.py and analyzer.py refer to the same file. Below is a short description of values to be stored and modified in the file.
1.   **Scan Start and Scan End** - Defines the Emulator Configuration Scan Start and End. These values help set the scope of the general range of the scan. See MRM API for more information. Scan Start should usually start at 0. 
2. **Base Integration Index** - Defines the Emulator Configuration Base Integration Index. See MRM API for more information.
3. **X and Y Values** - Defines the size of the image created. The image will be set to X meters by Y meters, where (0, 0) is the bottom left corner. The larger the X and Y values are, the more "zoomed out" the image will be. These values help define the image "frame".
4. **X_RES and Y_RES Values** - Defines the number of pixel the image will have. Forms a X_RES by Y_RES pixel image. Increasing these values increase resolution. 
5. **X_OFFSET and Y_OFFSET Values** - Defines the shift of the Axis in the image. The X_OFFSET value will shift the X-Axis by X_OFFSET meters to the left. The Y_OFFSET value will shift the Y-Axis Y_OFFSET meters down. These values help focus on the image.  
6. **Scan Amount**  - Defines the number of Scans that the emulator will do. See MRM API for more information.
7. **Skip** - Defines the number of scans that will be skipped over. 
8. **Contrast Value** - Increasing this value increases the contrast by taking all of the amplitudes in the pixel and raising it to the Contrast Value. A contrast Value of 1 is the default Contrast. 
9. **Transmit Gain** - Defines the Emulator Configuration Transmit Gain. See MRM API for more information. Default value is 63. 
10. **Scan Interval** - Defines the Emulator Configuration Scan Interal. See MRM API for more information. 

## Configuration Files - Analyzer Type
Analyer Type Config Files are used when directly running the Analyzer.py. Has less information compared to Emulator Type Config Files. Below is a short description of values to be stored and modified in the file.
1. **X and Y Values** - Defines the size of the image created. The image will be set to X meters by Y meters, where (0, 0) is the bottom left corner. The larger the X and Y values are, the more "zoomed out" the image will be.
2. **X_RES and Y_RES Values** - Defines the number of pixel the image will have. Forms a X_RES by Y_RES pixel image. Increasing these values increase resolution. 
3. **X_OFFSET and Y_OFFSET Values** - Defines the shift of the Axis in the image. The X_OFFSET value will shift the X-Axis by X_OFFSET meters to the left. The Y_OFFSET value will shift the Y-Axis Y_OFFSET meters down. These values help focus on the image. 
4. **Skip** - Defines the number of scans that will be skipped over. 
5. **Contrast Value** - Increasing this value increases the contrast by taking all of the amplitudes in the pixel and raising it to the Contrast Value. A Contrast Value of 1 is the default Contrast. 






# team2
Team 2 💪

Sign in sheet:  
Ty  
Tanush  
Jessica  
Ellie  
Felix  
