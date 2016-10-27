import numpy as np
import sys       
from obspy import read, Trace, Stream, UTCDateTime
from obspy.core.trace import Stats
from obspy.core import AttribDict
from obspy.segy.segy import SEGYTraceHeader, SEGYBinaryFileHeader
from obspy.segy.core import readSEGY

x = np.linspace(-np.pi, 10*np.pi, 151)
zeros=np.zeros(51)

streamtot=Stream()
stats = Stats()

for i in range(50):
    dato = np.sin(x+i*.1)
    dato = np.require(dato, dtype=np.float32)
    
    
    traces=Trace(data=dato, header={'delta': 0.004})
    traces.stats.delta=0.01
    traces.stats.starttime = UTCDateTime(2011,11,11,11,11,11)
    traces.stats.sampling_rate =20
    if not hasattr(traces.stats, 'segy.trace_header'):
        traces.stats.segy = {}
    traces.stats.segy.trace_header = SEGYTraceHeader()
    traces.stats.segy.trace_header.trace_sequence_number_within_line = i + 1
    traces.stats.segy.trace_header.receiver_group_elevation = 444

    
    traces.stats.segy.trace_header.lag_time_B = 154
    traces.stats.segy.trace_header.scalar_to_be_applied_to_times = -4
    traces.stats.segy.trace_header.sample_interval_in_ms_for_this_trace = 1
    traces.stats.segy.trace_header.number_of_samples_in_this_trace = len(traces)
    traces.stats.segy = AttribDict()
    traces.stats.segy.trace_header = AttribDict()
    traces.stats.segy.trace_header.uphole_time_at_group_in_ms = 66
    
    streamtemp=Stream(traces)
    
    streamtot+=streamtemp
    
    

streamtot.stats = AttribDict()
streamtot.stats.textual_file_header = 'Textual Header'
streamtot.stats.binary_file_header = SEGYBinaryFileHeader()
streamtot.stats.binary_file_header.number_of_data_traces_per_ensemble = 1
streamtot.stats.binary_file_header.trace_sorting_code = 5   
streamtot.stats.binary_file_header.number_of_samples_per_data_trace = len(streamtot[0])


print("Stream object before writing...")
streamtot.plot()
#streamtot.write('file.sgy', format='SEGY', data_encoding=1, byteorder=sys.byteorder)
#streamtot.write('file.segy', format='SEGY')
streamtot.write('file.segy', format='SEGY', data_encoding=1, byteorder=sys.byteorder)
