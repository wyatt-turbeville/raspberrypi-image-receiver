# Device Setup Instructions
### These instructions are for RaspberryPi hardware
1. Flash the appropriate RaspberryPi OS onto the device storage<br>
2. Connect the device to wifi<br>
   a. Optionally connect the device to RaspberryPi Connect for remote shell use.<br>
3. Install and connect to Tailscale<br>
   In terminal:<br>
   a. curl -fsSL https://tailscale.com/install.sh | sh<br>
   b. sudo tailscale up<br>
   c. follow the auth link and add the device to the same Tailnet as the file sending devices.<br>
4. Download the project files from github<br>
   In the home directory from terminal:<br>
   a. git clone https://github.com/wyatt-turbeville/raspberrypi-image-receiver.git<br>
5. Install the required libraries to a python virtual enviroment<br>
   In terminal:<br>
   Create a python virtual environment for dependencies<br>
   a. cd /directory/of/step/four<br>
   b. python3 -m venv .venv<br>
   c. source bin/scripts/activate<br>
   Install libraries to the virtual environment<br>
   d. pip install exif<br>
   e. pip install fastapi[standard]<br>
   f. pip install uvicorn<br>
   g. pip install python-multipart<br>
   These libraries may come preinstalled on some OS versions.<br>
6. Schedule the program as a system service (optional)<br>
   The concept here is to have the program continue running in the event the device gets interrupted in some way.<br>
   There are multiple methods to accomplish this, such as cron or autostart.<br>
   In terminal:<br>
   a. cd /directory/of/step/four<br>
   b. chmod +x install.sh<br>
   c. sudo ./install.sh<br>
   This shell script adds main.py as a systemd service to open every time the device is booted.<br>
