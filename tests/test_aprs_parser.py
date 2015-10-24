import unittest

from ogn.aprs_parser import parse_aprs


class TestStringMethods(unittest.TestCase):
    def test_server(self):
        parse_aprs("# aprsc 2.0.14-g28c5a6a 10 Apr 2015 18:58:47 GMT GLIDERN1 37.187.40.234:14580")

    def test_beacons(self):
        lines = list()
        lines.append(           "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5")
        lines.append(          "ICA4B0E3A>APRS,qAS,Letzi:/072319h4711.75N\\00802.59E^327/149/A=006498 id154B0E3A -3959fpm +0.5rot 9.0dB 0e -6.3kHz gps1x3")
        lines.append(  "Lachens>APRS,TCPIP*,qAC,GLIDERN2:/165334h4344.70NI00639.19E&/A=005435 v0.2.1 CPU:0.3 RAM:1764.4/2121.4MB NTP:2.8ms/+4.9ppm +47.0C RF:+0.70dB")
        lines.append(     "LFGU>APRS,TCPIP*,qAC,GLIDERN2:/190556h4907.63NI00706.41E&/A=000833 v0.2.0 CPU:0.9 RAM:281.3/458.9MB NTP:0.5ms/-19.1ppm +53.0C RF:+0.70dB")
        lines.append(          "FLRDDB091>APRS,qAS,Letzi:/195831h4740.04N/00806.01EX152/124/A=004881 id06DD8E80 +198fpm +0.0rot 6.5dB 13e +4.0kHz gps3x4")
        lines.append(     "LSGS>APRS,TCPIP*,qAC,GLIDERN1:/195345h4613.25NI00719.68E&/A=001581 CPU:0.7 RAM:247.9/456.4MB NTP:0.7ms/-11.4ppm +44.4C RF:+53+71.9ppm/+0.4dB")
        lines.append(           "FLRDDDD33>APRS,qAS,LFNF:/165341h4344.27N/00547.41E'/A=000886 id06DDDD33 +020fpm +0.0rot 20.8dB 0e -14.3kHz gps3x4")
        lines.append(           "FLRDDE026>APRS,qAS,LFNF:/165341h4358.58N/00553.89E'204/055/A=005048 id06DDE026 +257fpm +0.1rot 7.2dB 0e -0.8kHz gps4x7")
        lines.append(           "ICA484A9C>APRS,qAS,LFMX:/165341h4403.50N/00559.67E'/A=001460 id05484A9C +000fpm +0.0rot 18.0dB 0e +3.5kHz gps4x7")
        lines.append( "WolvesSW>APRS,TCPIP*,qAC,GLIDERN2:/165343h5232.23NI00210.91W&/A=000377 CPU:1.5 RAM:159.9/458.7MB NTP:6.6ms/-36.7ppm +45.5C RF:+130-0.4ppm/-0.1dB")
        lines.append(   "Oxford>APRS,TCPIP*,qAC,GLIDERN1:/190533h5142.96NI00109.68W&/A=000380 v0.1.3 CPU:0.9 RAM:268.8/458.6MB NTP:0.5ms/-45.9ppm +60.5C RF:+55+2.9ppm/+1.54dB")
        lines.append(         "OGNE95A16>APRS,qAS,Sylwek:/203641h5001.94N/01956.91E'270/004/A=000000 id07E95A16 +000fpm +0.1rot 37.8dB 0e -0.4kHz")
        lines.append(  "Salland>APRS,TCPIP*,qAC,GLIDERN2:/201426h5227.93NI00620.03E&/A=000049 v0.2.2 CPU:0.7 RAM:659.3/916.9MB NTP:2.5ms/-75.0ppm RF:+0.41dB")
        lines.append(     "LSGS>APRS,TCPIP*,qAC,GLIDERN1:/195345h4613.25NI00719.68E&/A=001581 CPU:0.7 RAM:247.9/456.4MB NTP:0.7ms/-11.4ppm +44.4C RF:+53+71.9ppm/+0.4dB")
        lines.append("Drenstein>APRS,TCPIP*,qAC,GLIDERN1:/203011h5147.51NI00744.45E&/A=000213 v0.2.2 CPU:0.8 RAM:695.7/4025.5MB NTP:16000.0ms/+0.0ppm +63.0C")
        lines.append(           "ZK-GSC>APRS,qAS,Omarama:/210202h4429.25S/16959.33E'/A=001407 id05C821EA +020fpm +0.0rot 16.8dB 0e -3.1kHz gps1x3 hear1084 hearB597 hearB598")

        for line in lines:
            result = parse_aprs(line)
            print(str(result), "\n")

if __name__ == '__main__':
    unittest.main()
