#!/usr/bin/env python
import os, glob, shutil, re
import txt_mixin
base_dir = '/home/ryan/git/controls/'
dist_dir = os.path.join(base_dir, 'dist')
dest_dir = '/home/ryan/siue/classes/450/2010/controls_dist/'
os.chdir(base_dir)

#delete old distributions
pats = ['controls*.exe', 'controls*.tar.gz']
del_dirs = [dist_dir, dest_dir]
for curdir in del_dirs:
    for pat in pats:
        cur_pat = os.path.join(curdir, pat)
        files = glob.glob(cur_pat)
        for path in files:
            os.remove(path)

#create new distribution
cmd1 = 'python setup.py sdist'
os.system(cmd1)
#cmd2 = 'python setup.py bdist_wininst'
cmd2 = 'python setup.py bdist --formats=wininst'
os.system(cmd2)

#copy to course dir for website

exe_pat = os.path.join(dist_dir, 'controls*.exe')
exe_files = glob.glob(exe_pat)
assert len(exe_files)==1, "Found more than one executable."
exe_file = exe_files[0]
junk, exe_name = os.path.split(exe_file)
win_name = re.sub('linux.*\\.exe','win32.exe',exe_name)
win_path = os.path.join(dest_dir, win_name)
shutil.copy2(exe_file, win_path)

gz_pat = os.path.join(dist_dir, 'controls*.tar.gz')
gz_files = glob.glob(gz_pat)
assert len(gz_files)==1, "Found more than one gz file."
gz_path = gz_files[0]
junk, gz_name = os.path.split(gz_path)
shutil.copy2(gz_path, dest_dir)
gz_dest_path = os.path.join(dest_dir, gz_name)

    
exe_re = '<controls_dist/controls-.*\\.exe>`_'
gz_re = '<controls_dist/controls-.*\\.tar\\.gz>`_'

exe_new = '<controls_dist/%s>`_' % win_name
gz_new = '<controls_dist/%s>`_' % gz_name

rst_path = '/home/ryan/siue/classes/450/2010/python.rst'
myfile = txt_mixin.txt_file_with_list(rst_path)
myfile.replaceallre(exe_re, exe_new)
myfile.replaceallre(gz_re, gz_new)
myfile.save(rst_path)

fne, ext = os.path.splitext(rst_path)
html_path = fne + '.html'
rstcmd = 'rst2html %s %s' % (rst_path, html_path)
print(rstcmd)
os.system(rstcmd)


