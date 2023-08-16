# fllrig_scanner
Scan frequency ranges and lists exploiting FLRIG XML-RPC


## Data Format
The scan raanges are defined as CSV or in-line as:

### example csv file
```
band,low,high,mode,bw,sq
80m,3500000,3800000,LSB,1000,10
pmr,446006250,446193750,FM,12500,10
2ms,145350000,145600000,FM,12500,32
air1,119250000,119950000,AM,10000,20
```

## Typical Output
```
G0FOZ Rig scanner-->flrig @http://localhost:12346 version: 1.4.7
Current frequency: 446168750  S Meter: 0  Info: R:IC-7000 T:R FA:0 M:FM L:50 U: N:812 Vol:41 Mic:56 Rfg:100 
80m : 3500000 --> 3800000 size 1000 sq 10 mode LSB
pmr : 446006250 --> 446193750 size 12500 sq 10 mode FM
2ms : 145350000 --> 145600000 size 12500 sq 32 mode FM
air1 : 119250000 --> 119950000 size 10000 sq 20 mode AM
Current freq: 446168750. Enter to scan this band, or enter a band from list above: 
set mode FM start 446006250 to 446193750
Signal 47 > 10 dB. Scan stopped (16/08/2023 12:01:33). Frequency (pmr) is 446.10625MHz
Signal 0 < 10 dB. Scaning restarted (16/08/2023 12:01:33) after 5.38S
Signal 58 > 10 dB. Scan stopped (16/08/2023 12:01:59). Frequency (pmr) is 446.10625MHz
Signal 0 < 10 dB. Scaning restarted (16/08/2023 12:01:59) after 7.97S
```


