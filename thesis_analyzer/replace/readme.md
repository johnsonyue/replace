##modular:
 * trace defines **one unified** data format used to store raw trace data.
   * design: put hard-coded content in one file,
   * advantages:
     * minimize confusion
     * better readability
     * easier to swap,add,rm fields
 * to add new data sources (e.g. CAIDA, iPlane, RIPE Atlas ..),
   * implement decoding method in decode.sh
   * implement uniform method in uniform.py
 * to add new data fields to trace:
   * add field index to trace.py
   * modify uniform methods in uniform.py
   * modify analyze methods in analyze.py
