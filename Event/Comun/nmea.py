from twisted.python import log
import operator,sys

class gpsGPRMC():
    def parsegprmc(self,line):
        """
        line = Un linea geom tipo GPRMC
        return = Lista de ((latitude,longitude,utc,status,speed,course,utcdate,magvar),checksum)
        --------
        
        """
        strmessage, checksum = line[0:].strip().split('*')
        validchecksum, checksum, calculated_checksum = True,int(checksum, 16), reduce(operator.xor, map(ord, strmessage))
        
        if checksum != calculated_checksum:
                log.msg("Given 0x%02X != 0x%02X" % (checksum, calculated_checksum))
                validchecksum = False
        m = strmessage.split(',')
        if list(m)[0].startswith('$GPRMC'):
            m.pop(0)
        elif list(m)[0].startswith('GPRMC'):
            m.pop(0)
        else:
            pass
        #m=re.match(reg, line)
        return self.decode_positiontime(list(m)[0],list(m)[1],list(m)[2], list(m)[3], list(m)[4], list(m)[5],list(m)[6],list(m)[7],list(m)[8],list(m)[9],list(m)[10]),validchecksum

    def _decode_utc(self, utc):
        utc_hh, utc_mm, utc_ss = map(float, (utc[:2], utc[2:4], utc[4:]))
        return utc_hh * 3600.0 + utc_mm * 60.0 + utc_ss

    def _decode_latlon(self, latitude, ns, longitude, ew):
        latitude = float(latitude[:2]) + float(latitude[2:])/60.0
        if ns == 'S':
            latitude = -latitude
        longitude = float(longitude[:3]) + float(longitude[3:])/60.0
        if ew == 'W':
            longitude = -longitude
        return (latitude, longitude)
    def _decode_speed(self,speed):
        if speed != '':
            speed = float(speed)
        else:
            speed = None
        return speed
    
    def decode_positiontime(self, utc, status, latitude, ns, longitude, ew, speed, course, utcdate, magvar,magdir):
        latitude, longitude = self._decode_latlon(latitude, ns, longitude, ew)
        utc = self._decode_utc(utc)
        if status == 'A':
            status = 1
        else:
            status = 0
        speed = self._decode_speed(speed)
        if course != '':
            course = float(course)
        else:
            course = None
        utcdate = 2000+int(utcdate[4:6]), int(utcdate[2:4]), int(utcdate[0:2])
        
        if magvar != '':
            magvar = float(magvar)
            
        if magdir.startswith('W'):
            magvar = -magvar
        else:
            magvar = None
        return (
            latitude,
            longitude,
            utc,
            status,
            speed,
            course,
            utcdate,
            magvar,
        )

if __name__== "__main__":
    log.startLogging(sys.stdout);
    print gpsGPRMC().parsegprmc("$GPRMC,165844.00,A,4325.295910,N,00549.202648,W,0.0,0.0,081112,4.3,W,A*25")
    print gpsGPRMC().parsegprmc("$GPRMC,120500.000,A,6000.0000,N,13000.0000,E,20.00,0.00,010112,,*33")
    print gpsGPRMC().parsegprmc("$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E,A*2B")
    print gpsGPRMC().parsegprmc("GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E,A*2B")
    print gpsGPRMC().parsegprmc("$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62")
    print gpsGPRMC().parsegprmc("$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68")
    print gpsGPRMC().parsegprmc("$GPRMC,094429.000,A,4325.2970,N,00549.1990,W,0.00,0.00,051212,,*13")
    
    
    
