export CUDA_VISIBLE_DEVICES=''

CheckScore:
	python3 test_yahtzee.py 20000 < training.dat | grep "RESULT" | cut -c9- > score.txt
	cp /c/cs474/hw6/CheckScore .
