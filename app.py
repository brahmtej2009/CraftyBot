#Copyright 2026 Brahmtej Singh

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import os
import subprocess
import time

if os.environ.get("CRAFTYBOT_RUNNING") != "1":
    os.environ["CRAFTYBOT_RUNNING"] = "1"
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__,
                    "--client.toolbarMode=developer",
                    "--server.runOnSave=true",
                    "--server.fileWatcherType=poll"])
    sys.exit()


import streamlit as st
import socket
from mcstatus import JavaServer as jsrv

st.set_page_config(
    page_title="CraftyBot",
    page_icon="🌐",
    layout="wide"
)


st.markdown("""
<style>

header, [data-testid="stHeader"] { display: none !important; }

.block-container {
    padding-top: 2rem;
}

[data-testid="stDecoration"] { display: none !important; }

[data-testid="stToolbar"], [data-testid="stStatusWidget"],
.stDeployButton, [data-testid="stAppDeployButton"] { display: none !important; }

.block-container { padding-top: 1rem !important; }
[data-testid="stAppViewContainer"] { margin-top: 0 !important; }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid="stVerticalBlock"] {
    gap: 0.5rem;               /* default is 1rem */
}
h1, h2, h3 {
    padding-top: 0.8rem !important;
    padding-bottom: 0.1rem !important;
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
# Welcome to CraftyBot
##### Minecraft Server Status Checking Tool<br>""",unsafe_allow_html=True)



    
def chksrv(serverip):
    if not serverip:
        st.error('Please enter an IP before continuing.')
    else:

        try:

            srv=jsrv.lookup(serverip, timeout=3)

            status=srv.status()
            st.write(f"""
------------------------------------------------------
# Check For {serverip}
### Online players: {status.players.online}
### Max players: {status.players.max}
### Server version: {status.version.name}
### MOTD: {status.motd.to_plain()}
### Your Latency to Server: {round(status.latency)} ms
------------------------------------------------------
""")
        except socket.gaierror as e:
            st.error(f"Server with IP {serverip} is not valid.")
        except (TimeoutError, ConnectionRefusedError, OSError) as e:
            st.error("The Server is Offline")
        except Exception as e:
            st.error(f"Unknown Error {e} Occurred.")
            
        
    
col1,col2=st.columns(2,gap="xsmall",vertical_alignment='center')
serverip= col1.text_input("Enter Server's IP Here",placeholder="mc.hypixel.net")

if len(serverip.split("."))<2:
    st.error("Entered Server IP is not valid. Please enter a correct domain or a subdomain.")

btn=col2.button("Search Server",key="1")
ltchk=col2.button("Test latency",key="2")
if btn:
    with st.spinner("Fetching all server data... Please wait"):
        chksrv(serverip.strip())
if ltchk:
    with st.spinner("Pinging server and calculating latency... Please wait"):
        chk_n=5
        lat=[]
        for d in range(chk_n):
            srv=jsrv.lookup(serverip, timeout=5)
            status=srv.status()
            lat.append(status.latency)
            time.sleep(1)
        sm=0
        for i in lat:
            sm+=i
        av_latency=round(sm/chk_n)
        st.write(f"Average latency to {serverip} is {av_latency} ms")