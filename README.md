# TimeSeries-Spliter
An easy TimeSeries spliter into "size" batches. 

## Quick-start

<p> You should have all your legitimate and DDoS TimeSeries stored in diferent folders.
The format should looks like: </p>
<pre> 
    <date>_<time>-<metric>-<granularity>

    Example:
    2018-03-29_18.06.20-difInput_OutputBytes-60000 
</pre>

## Software skills

<ul>
<li> Build a folder where you have all your granularities together (diferent folder eachone)</p>
<li> Store all metric folders inside the corresponding granularities</p>
<li> Finally, inside metric folders, all the TimeSeries will be saved inside "Legitimo" or "DDoS" folders.</p>
</ul>

## Final dataset structure

<p>Data should looks like: </p>

<pre>
    Granualrity1
    Granularity2
    Granularity2
        |
        - - - - metric1
                metric2
                metric3
                   |
                   - - -  timeserie1
                          timeserie2
                          timeserie3
                              .
                              .
                              .
</pre>

## Divide TimeSeries into specific **size batches**

<p>Go to projects folder and fire up a terminal: </p>
<pre>
    python divider.py <dataset root folder> <size>
    
    Example:
    python divider.py /home/andres/dataset 150
</pre>
<p> *NOTE: "size" is the number of elements every new timeseries will have. </p>

## Separete TimeSeries into granularity and metrics
