import os, shlex, subprocess

svgDir = "/home/will/workspace/MX-Mariner/iconsrc/regions/nga/"
drawableDir = "/home/will/workspace/MX-Mariner/res/drawable/"

command = "inkscape --without-gui --export-png=%s.png --export-dpi=72 --export-background-opacity=0 --export-width=80 --export-height=80 \"%s.svg\""

for svg in os.listdir(svgDir):
    if svg.endswith(".svg"):
        region = svg.rstrip(".svg")
        #print shlex.split(command %(drawableDir+region, svgDir+region))
        thisone = subprocess.Popen(shlex.split(command %(drawableDir+region, svgDir+region)))
        thisone.wait()