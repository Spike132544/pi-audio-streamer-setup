# Pi Audio Streamer
# Cal Poly - Senior Project
# Daniel Macias and Stefan Patch

import re

def wpa_supplicant_update(country, SSID, password):
    wpa_template =  open('resources/wpa_supplicant.template', 'r+')
    text = wpa_template.read()
    text = re.sub('<UserCountry>', country, text)
    text = re.sub('<UserSSID>', SSID, text)
    text = re.sub('<UserPassword>', password, text)
    wpa_template.close()

    wpa_conf = open('resources/wpa_supplicant.conf', 'x')
    wpa_conf.write(text)
    wpa_conf.close()


def config_txt_update(filepath):
    config_txt = open(filepath, 'a')
    config_txt.write('\n')
    config_txt.write('dtoverlay=dwc2')
    config_txt.close()


def cmdline_txt_update(filepath):
    config_txt = open(filepath, 'a')
    config_txt.write(' modules-load=dwc2,g_ether')
    config_txt.close()


def main():
    wpa_supplicant_update('US', 'ThisIsAUsername', 'P@ssW0rD999')
    config_txt_update('/config.txt')
    cmdline_txt_update('/cmdline.txt')


if __name__ == '__main__':
    main()