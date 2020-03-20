
from datetime import datetime
import codecs

fileName = './Traces/trace.log'

def log(trace):
    with codecs.open(fileName, mode='a+', encoding='utf-8') as f_out:
        f_out.write(str(datetime.now()) + '    ' + trace + "\n")

if __name__ == "__main__":
    log("Hello")
    log("World")
        