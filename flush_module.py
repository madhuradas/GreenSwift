import os
from os import listdir
from os.path import basename, dirname, isdir, isfile, join
import random
import time
import cPickle as pickle
from eventlet import Timeout
from eventlet.green import subprocess
from swift.common.utils import rsync_ip

def del_dict():
	f = pickle.load(open('/usr/bin/device.p','rb'))
	f= {}
	pickle.dump(f,open('/usr/bin/device.p','wb'))


def rsync(partition, device, suffix):
        node_ip = rsync_ip('127.0.0.1')
        rsync_module = '%s::object' %(node_ip)
        spath = join('/srv/node/ssd/objects/%s' %(partition),suffix[1])
	print(suffix)
        args = [
            'rsync',
            '--recursive',
            '--whole-file',
            '--human-readable',
            '--xattrs',
            '--itemize-changes',
            '--ignore-existing',
            '--timeout=30',
            '--contimeout=30',
        ]
        args.append(spath)
        args.append(join(rsync_module, device, 'objects', partition))
	start_time = time.time()
        ret_val = None
        try:
                with Timeout(900):
                    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    results = proc.stdout.read()
                    ret_val = proc.wait()

        except Timeout:
            print("Killing long-running rsync: %s", str(args))
            proc.kill()
            return 1
	total_time = time.time() - start_time
        for result in results.split('\n'):
            if result == '':
                continue
            if result.startswith('cd+'):
                continue
	    if not ret_val:
                print(result)
            else:
                print(result)
        if ret_val:
            print('Bad rsync return code: %(args)s -> %(ret)d',
                              {'args': str(args), 'ret': ret_val})
        elif results:
            print("Successful rsync of %(src)s at %(dst)s (%(time).03f)",
                {'src': args[-2], 'dst': args[-1], 'time': total_time})
        else:
            print("Successful rsync of %(src)s at %(dst)s (%(time).03f)",
                {'src': args[-2], 'dst': args[-1], 'time': total_time})
        return ret_val
def flush():
	dict_info = pickle.load(open('/usr/bin/device.p','rb'))
	print dict_info
	files = [f for f in listdir('/srv/node/ssd/objects')] 
	for f in files:
	     deviceList = dict_info[f]
	     suffix = listdir('/srv/node/ssd/objects/%s'%(f))
	     for i in deviceList:
	            os.system('mkdir -p /srv/node/%s/objects/%s/%s' %(i,f,suffix[1]))
	os.system('chown -R swift:swift /srv/node')
	for f in files:
	     deviceList = dict_info[f]
	     suffix = listdir('/srv/node/ssd/objects/%s'%(f))
	     for i in deviceList:
	            rsync(f,i,suffix)
	print "flush done.... deleting dictionary"
	del_dict()
