#!/usr/bin/env python
import glob
import os
import shutil
import tarfile 
import sys
from DataModelDict import DataModelDict as DM

def main(*args):
    
    #Read in input script terms
    run_directory, lib_directory = __initial_setup(*args)

    for simmy in glob.iglob(os.path.join(lib_directory, '*', '*', '*', '*', '*.tar.gz')):
        try:
            tarry = tarfile.open(simmy, 'r:gz')
            tarry.extractall(run_directory)
            tarry.close()
            os.remove(simmy)
        except:
            print 'Failed to extract', simmy
            tarry.close()            
        
    for biddy in glob.iglob(os.path.join(run_directory, '*', '*.bid')):
        os.remove(biddy)
    for result in glob.iglob(os.path.join(run_directory, '*', 'results.json')):
	os.remove(result)

    for record in glob.iglob(os.path.join(run_directory, '*', '*.json')):
        with open(record) as f:    
            model = DM(f)
        key = model.keys()[0]
        try:
            if model[key]['status'] == 'error':
                model[key]['status'] = 'not calculated'
                del(model[key]['error'])
                with open(record, 'w') as f:
                    model.json(fp=f, indent=4)
        except:
            pass

    for record in glob.iglob(os.path.join(lib_directory, '*', '*', '*', '*', '*.json')):
        with open(record) as f:
            model = DM(f)
        key = model.keys()[0]
        try:
            if model[key]['status'] == 'error':
                model[key]['status'] = 'not calculated'
                del(model[key]['error'])
                with open(record, 'w') as f:
                    model.json(fp=f, indent=4)
        except:
            pass

    
def __initial_setup(*args):            
    run_directory = None
    lib_directory = None
    with open(args[0]) as f:
        for line in f:
            terms = line.split()
            if len(terms) > 0 and terms[0][0] != '#':
                if terms[0] == 'run_directory' and run_directory is None:
                    run_directory = ' '.join(terms[1:])
                elif terms[0] == 'lib_directory' and lib_directory is None:
                    lib_directory = ' '.join(terms[1:])
                else:
                    raise ValueError('Invalid runner.py input line')
    if run_directory is not None and lib_directory is not None:
        return run_directory, lib_directory
    else:
        raise ValueError('clean.py input requires both run_directory and lib_directory')
    
if __name__ == '__main__':
    main(*sys.argv[1:])    
