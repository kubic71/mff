STUDENT_ID = 32

.PHONY: test
test: splay_experiment.py
	# @rm -rf out && mkdir out
	@for test in sequential random subset ; do \
		for mode in std naive ; do \
			echo t-$$test-$$mode ; \
			./splay_experiment.py $$test $(STUDENT_ID) $$mode >out/t-$$test-$$mode ; \
		done ; \
	done

.PHONY: clean
clean:
	# rm -rf out
