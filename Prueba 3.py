from obspy.core import read, Trace, AttribDict, Stream, UTCDateTime
from obspy.segy.segy import SEGYTraceHeader, SEGYBinaryFileHeader
from obspy.segy.core import readSEGY
import numpy as np
import sys
import segy
stream = Stream()

for _i in range(3):
    # Create some random data.
    data = np.random.ranf(1000)
    data = np.require(data, dtype='float32')
    trace = Trace(data=data)
    # Attributes in trace.stats will overwrite everything in
    # trace.stats.segy.trace_header
    trace.stats.delta = 0.01
    # SEGY does not support microsecond precission! Any microseconds will be
    # discarded.
    trace.stats.starttime = UTCDateTime(2011,11,11,11,11,11)
    
    # If you want to set some additional attributes in the trace header, add
    # one and only set the attributes you want to be set. Otherwise the header
    # will be created for you with default values.
    if not hasattr(trace.stats, 'segy.trace_header'):
        trace.stats.segy = {}
    trace.stats.segy.trace_header = SEGYTraceHeader()
    trace.stats.segy.trace_header.trace_sequence_number_within_line = _i + 1
    trace.stats.segy.trace_header.receiver_group_elevation = 444
    
    # Add trace to stream
    stream.append(trace)
stream.stats = AttribDict()
stream.stats.textual_file_header = 'Textual Header!'
stream.stats.binary_file_header = SEGYBinaryFileHeader()
stream.stats.binary_file_header.trace_sorting_code = 5

print("\nStream object before writing...")
print(stream)

stream.write("TEST.sgy", format="SEGY", data_encoding=1, byteorder=sys.byteorder)
