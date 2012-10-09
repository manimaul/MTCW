import sys, subprocess, shlex, os, shutil
import Regions, Env

command = "python %s%s %s"

def doItAll(region):
    if Regions.isRegion(region):
        cmd = shlex.split( command %( Env.mtcwDir, "BatchRegionTiler.py", region) )
        subprocess.Popen(cmd).wait()
        
        cmd = shlex.split( command %( Env.mtcwDir, "BatchRegionMerger.py", region) )
        subprocess.Popen(cmd).wait()
        
        if len(Regions.getRegionFilterList(region)) == len(open(Env.mergedTileDir+region+"/mergeorder.txt").readlines()):
        
            cmd = shlex.split( command %( Env.mtcwDir, "BatchRegionOptimizer.py", region) )
            subprocess.Popen(cmd).wait()
            
            cmd = shlex.split( command %( Env.mtcwDir, "AutoGemf.py", region) )
            subprocess.Popen(cmd).wait()
            
            if os.path.isdir(Env.mergedTileDir+region):
                shutil.rmtree(Env.mergedTileDir+region)
                
            if os.path.isdir(Env.mergedTileDir+region+".opt"):
                shutil.rmtree(Env.mergedTileDir+region+".opt")
                
            cmd = shlex.split( command %( Env.mtcwDir, "GenerateMxRegionData.py", region) )
            subprocess.Popen(cmd).wait()
            
        else:
            print len(Regions.getRegionFilterList(region))
            print len(open(Env.mergedTileDir+region+"/mergeorder.txt").readlines())
            print "an error occurred"

if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        doItAll(sys.argv[1])