SDIR = quiz
UDIR = utils
MUDIR = myutils
TDIR = tests
SRCS = $(SDIR)/apps.py $(SDIR)/models.py

prod: $(SRCS)
# run tests here before building!
	-git commit -a
	git push origin master
	ssh devopscourse@ssh.pythonanywhere.com 'cd /home/devopscourse/mysite; /home/devopscourse/mysite/myutils/prod.sh'

