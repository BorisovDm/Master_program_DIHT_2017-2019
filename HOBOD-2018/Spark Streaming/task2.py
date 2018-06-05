from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from ua_parser import user_agent_parser
import hyperloglog


def ls(directory):
    hadoop = sc._jvm.org.apache.hadoop
    fs = hadoop.fs.FileSystem
    conf = hadoop.conf.Configuration()
    path = hadoop.fs.Path(directory)
    return [f.getPath() for f in fs.get(conf).listStatus(path)]


def update_func(new_values, state):
    state = state or hyperloglog.HyperLogLog(0.05)

    for value in new_values:
        state.add(value)
    return state


def check_rdd(rdd):
    global this_is_the_end
    if rdd.isEmpty():
        this_is_the_end = True


def map_seg(x):
    if 'iPhone' in user_agent_parser.Parse(x[4])['device']['family']:
        return 'seg_iphone', x[1]
    if 'Firefox' in user_agent_parser.Parse(x[4])['user_agent']['family']:
        return 'seg_firefox', x[1]
    if 'Windows' in user_agent_parser.Parse(x[4])['os']['family']:
        return 'seg_windows', x[1]


def print_info(rdd):
    global this_is_the_end
    if this_is_the_end:
        for seg, uid_set in rdd:
            print('%s\t%d' % (seg, uid_set.card()))


sc = SparkContext(master='local[4]')
ssc = StreamingContext(sc, batchDuration=10)
ssc.checkpoint("test_checkpoint")

this_is_the_end = False
files = ls("hdfs:///data/course4/page_view_1m_splitted_by_10k")
queueRDD = [ssc.sparkContext.textFile(str(f)) for f in files]

dstream = ssc.queueStream(queueRDD)
dstream.foreachRDD(lambda rdd: check_rdd(rdd))

seg = dstream \
        .map(lambda x: x.strip().split("\t")) \
        .map(lambda x: map_seg(x)) \
        .filter(bool) \
        .updateStateByKey(update_func) \
        .foreachRDD(lambda x: print_info(x.collect()))

ssc.start()

while not this_is_the_end:
    pass

ssc.stop()