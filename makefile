# Need to export as ENV var
export TEMPLATE_DIR = templates

UDIR = utils
TDIR = tests
SRCS = $(SDIR)/arithmetic.py $(SDIR)/control_flow.py $(SDIR)/data_mov.py $(SDIR)/interrupts.py 

prod: $(SRCS)
# run tests here before building!
	-git commit -a
	git push origin master
	ssh devopscourse@ssh.pythonanywhere.com 'cd /home/devopscourse/mysite; /home/devopscourse/mysite/myutils/prod.sh'

