import pyvisa
import numpy as np
from pyvisa import Resource

rm = pyvisa.ResourceManager()

def scope_connection() -> Resource:
    ip_address = '192.168.1.20'  # IP address in LAN 
    visa_address = f'TCPIP0::{ip_address}::inst0::INSTR'
    try:
        scope = rm.open_resource(visa_address)
        #print(f"Successfully connected: {scope.query('*IDN?')}")
    except pyvisa.VisaIOError:
        print(f" Can't find the equipment in {visa_address} ")
    return scope

def func_gen_connection():
    func_gen_visa = 'GPIB0::11::INSTR' #Address of GPIB connection
    try:
        func_gen = rm.open_resource('GPIB0::11::INSTR')
        #print(f"Successfully connected: {func_gen.query('*IDN?')}")
    except pyvisa.VisaIOError:
        print(f"Can't find the equipment in {func_gen_visa}")
    return func_gen

def func_gen_setting_edge_modify(func_gen,pulse_width, voltage, low,trailing_width):
    ''' Due to SCIP function generation rule, edge of the pulses are intersected at the point 90 %. 
    Thus, the edge should be modified. '''
  
    input_trailing_width = 0.8 * trailing_width* ((voltage-low)/voltage)
    input_pulse_width = pulse_width + 0.5 * trailing_width * ((voltage-low)/voltage) 
    func_gen.write('*RST')#func_gen setting reset
    func_gen.write(f'SOURce1:PULSe:PERiod {input_pulse_width*2}s')
    func_gen.write(f'SOURce2:PULSe:PERiod {input_pulse_width*2}s')
    func_gen.write(f'SOURce1:PULSe:WIDth {input_pulse_width}s')
    func_gen.write(f'SOURce2:PULSe:WIDth {input_pulse_width}s')
    func_gen.write(f'SOURce1:BURst:MODE TRIgered')
    func_gen.write(f'SOURce1:BURst:NCYCles 1')
    func_gen.write(f'SOURce2:BURst:MODE TRIgered')
    func_gen.write(f'SOURce2:BURst:NCYCles 1')
    func_gen.write('SOURce1:FUNCtion:SHAPe PULSe')
    func_gen.write('SOURce2:FUNCtion:SHAPe PULSe')
    trailing = input_trailing_width
    func_gen.write(f'SOURce1:PULSe:TRANsition:TRAIling {trailing}s')
    func_gen.write(f'SOURce2:PULSe:TRANsition:TRAIling {trailing}s')

    if voltage > 0:
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:High {voltage}')
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:Low {low}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:High {voltage}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:Low {low}')
    else:
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:High {low}')
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:Low {voltage}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:High {low}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:Low {voltage}')
    func_gen.write(f'SOURce1:BURst:STATe ON')
    func_gen.write(f'SOURce2:BURst:STATe ON')

def func_gen_setting_leading_edge_modify(func_gen,pulse_width, voltage, low,leading_width):
    ''' Due to SCIP function generation rule, edge of the pulses are intersected at the point 90 %. 
    Thus, the edge should be modified. '''
    input_leading_width = 0.8 * leading_width* ((voltage-low)/voltage)
    input_pulse_width = pulse_width + 0.5 * leading_width * ((voltage-low)/voltage)
    func_gen.write('*RST')#func_gen setting reset
    func_gen.write(f'SOURce1:PULSe:PERiod {input_pulse_width*2}s')
    func_gen.write(f'SOURce2:PULSe:PERiod {input_pulse_width*2}s')
    func_gen.write(f'SOURce1:PULSe:WIDth {input_pulse_width}s')
    func_gen.write(f'SOURce2:PULSe:WIDth {input_pulse_width}s')
    func_gen.write(f'SOURce1:BURst:MODE TRIgered')
    func_gen.write(f'SOURce1:BURst:NCYCles 1')
    func_gen.write(f'SOURce2:BURst:MODE TRIgered')
    func_gen.write(f'SOURce2:BURst:NCYCles 1')
    func_gen.write('SOURce1:FUNCtion:SHAPe PULSe')
    func_gen.write('SOURce2:FUNCtion:SHAPe PULSe')
    func_gen.write(f'SOURce1:PULSe:TRANsition:leading {input_leading_width}s')
    func_gen.write(f'SOURce2:PULSe:TRANsition:leading {input_leading_width}s')

    if voltage > 0:
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:High {voltage}')
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:Low {low}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:High {voltage}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:Low {low}')
    else:
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:High {low}')
        func_gen.write(f'SOURce1:VOLTage:LEVel:IMMediate:Low {voltage}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:High {low}')
        func_gen.write(f'SOURce2:VOLTage:LEVel:IMMediate:Low {voltage}')
    func_gen.write(f'SOURce1:BURst:STATe ON')
    func_gen.write(f'SOURce2:BURst:STATe ON')

def func_gen_output(func_gen):
    #synchronize ch1 and ch 2
    func_gen.write('SOURce1:PHASe:INITiate')
    func_gen.write('SOURce2:PHASe:INITiate')
    func_gen.write('OUTPUT1:STATE on')
    func_gen.write('OUTPUT2:STATE on')

def func_gen_off(func_gen):
    func_gen.write('OUTPut1 OFF')  
    func_gen.write('OUTPut2 OFF')
    func_gen.write('*RST')
    func_gen.close()

def scope_setting_trailing_edge(scope, pulse_width, voltage,low):
    data = 100000 # data aquisition point 
    scope.write('ACQUIRE:STATE OFF')
    scope.write('SELECT:CH1 ON') 
    scope.write('SELECT:CH2 ON')
    scope.write('CH1:INVert OFF')
    scope.write('CH2:INVert ON') #Polarity chage of ch2, Our PMT signal is lower than 0
    scope.write('ACQUIRE:MODE SAMPLE')
    scope.write(f'HORizontal:RECOrdlength {data}')
    scope.write(f'HORIZONTAL:SCALE {pulse_width/2}')
    scope.write('DATA:START 1')
    scope.write(f'DATA:STOP {data}')  
    scope.write(f'CH1:SCALE 2')
    scope.write(f'CH2:SCALE 0.8')
    scope.write('ACQUIRE:STATE ON')
    # Triggering methods
    scope.write('TRIGGER:A:TYPE EDGE')
    # Trigger source --> Ch1 
    scope.write('TRIGGER:A:EDGE:SOURCE CH1')
    scope.write('TRIGGER:A:EDGE:SLOPE rise')
    scope.write(f'TRIGGER:A:LEVEL {(low +voltage) /2}')


def scope_setting_leading_edge(scope, pulse_width, voltage,low):
    data = 100000
    scope.write('ACQUIRE:STATE OFF')
    scope.write('SELECT:CH1 ON')
    scope.write('SELECT:CH2 ON')
    scope.write('CH1:INVert OFF')
    scope.write('CH2:INVert ON')
    scope.write('ACQUIRE:MODE SAMPLE')
    scope.write(f'HORizontal:RECOrdlength {data}')
    scope.write(f'HORIZONTAL:SCALE {pulse_width/2}')
    scope.write('DATA:START 1')
    scope.write(f'DATA:STOP {data}')  
    scope.write(f'CH1:SCALE 2')
    scope.write(f'CH2:SCALE 0.8')
    scope.write('ACQUIRE:STATE ON')
    scope.write('TRIGGER:A:TYPE EDGE')
    scope.write('TRIGGER:A:EDGE:SOURCE CH1')
    scope.write('TRIGGER:A:EDGE:SLOPE fall')
    scope.write(f'TRIGGER:A:LEVEL {(low +voltage) /2}')

def scope_ascii_measure(scope):
    # Read data from CH1
    scope.write('DATA:SOURCE CH1')
    scope.write('DATa:ENCdg ASCII')  # Switch to ASCII encoding
    raw_response = scope.query('CURVe?')
    numeric_data = raw_response[7:].split(' ')[-1]  # Modify this based on the actual format
    y1_ascii = np.array([float(val) for val in numeric_data.split(',')])
    # Retrieve scale factors for CH1
    y1mult = float(scope.query('WFMPRE:YMULT?').split()[-1])
    y1zero = float(scope.query('WFMPRE:YZERO?').split()[-1])
    y1off = float(scope.query('WFMPRE:YOFF?').split()[-1])
    # Process data for CH1 (apply scale factors)
    y1_processed = (y1_ascii - y1off) * y1mult + y1zero
    # Read data from CH2
    scope.write('DATA:SOURCE CH2')
    raw_response = scope.query('CURVe?')
    numeric_data = raw_response[7:].split(' ')[-1]  # Modify this based on the actual format
    y2_ascii = np.array([float(val) for val in numeric_data.split(',')])
    # Retrieve scale factors for CH2
    y2mult = float(scope.query('WFMPRE:YMULT?').split()[-1])
    y2zero = float(scope.query('WFMPRE:YZERO?').split()[-1])
    y2off = float(scope.query('WFMPRE:YOFF?').split()[-1])
    # Process data for CH2 (apply scale factors)
    y2_processed = (y2_ascii - y2off) * y2mult + y2zero
    # Calculate X increment (ensure the scope buffer size matches your data range)
    xincr = float(scope.query('WFMOutPRE:XINCR?').split()[-1])
    # Generate the X data based on the X increment and the number of data points
    x_data = np.arange(0, xincr * len(y1_processed), xincr)*1E6
    return [x_data, y1_processed/2, y2_processed/2]

def scope_off(scope):
    scope.write('ACQuire:STATE OFF')
    scope.write('*RST')
    scope.close()
