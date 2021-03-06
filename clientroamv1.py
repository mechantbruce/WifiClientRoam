'''
Client Roaming script v1.0
Displays wireless statistics from host PC

2017 Cisco Advanced Services
Michal Kowalik / Bruce McMurdo
'''
import subprocess, time, re, os

def apple():
    command = 'exec /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I'
    output = subprocess.check_output(command,shell=True)
    try:
        ssid = 'SSID:' + re.search(r' SSID.+', output).group(0).split()[-1]
        bssid = 'BSSID:' + re.search(r'BSSID.+', output).group(0).split()[-1]
        channel = 'Ch:' + re.search(r'channel.+', output).group(0).split()[-1]
        txrate = 'TX:' + re.search(r'lastTxRate.+', output).group(0).split()[-1]
        signal = 'Signal:' + re.search(r'CtlRSSI.+', output).group(0).split()[-1]  
        noise = 'Noise' + re.search(r'agrCtlNoise.+', output).group(0).split()[-1]   
        signal1 = int(re.search(r'CtlRSSI.+', output).group(0).split()[-1])
        noise1 = int(re.search(r'agrCtlNoise.+', output).group(0).split()[-1])
        SNR = 'SNR:' + str( signal1 - noise1 )
    except AttributeError:
        print 'No data'
        pass
    clock = time.asctime().split()[3]
    print clock, ssid, bssid, channel, txrate, noise, signal, SNR
    time.sleep(1)

def microsoft():
    wifi = True
    output = subprocess.check_output('netsh wlan show interfaces')
    try:
        ssid = 'SSID:' + re.search(r'SSID.+', output).group(0).split()[-1]
        bssid = 'BSSID:' + re.search(r'BSSID.+', output).group(0).split()[-1]
        channel = 'Ch:' + re.search(r'Channel.+', output).group(0).split()[-1]
        txrate = 'TX:' + re.search(r'Transmit.+', output).group(0).split()[-1]
        rxrate = 'RX:' + re.search(r'Receive.+', output).group(0).split()[-1]
        signal = re.search(r'Signal.+', output).group(0).split()[-1][:-1]          
    except AttributeError:
        print 'No data'
        wifi = False
        pass
    clock = time.asctime().split()[3]
    if wifi:
        dbm = 'dBm:' + str(int(signal) / 2 - 100)
        print clock, ssid, bssid, dbm, channel, txrate, rxrate
    wifi = True
    time.sleep(0.5)

operating_system = os.name
try:
    while True:
        if operating_system == 'posix': apple()
        if operating_system == 'nt': microsoft()
except KeyboardInterrupt:
    print 'Script stopped.'

    


