ab_tree_test: ab_tree_test.cpp ab_tree.h test_main.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

test: ab_tree_test
	./$<

# CXXFLAGS=-std=c++11 -O2 -Wall -Wextra -g -Wno-sign-compare
CXXFLAGS=-std=c++11 -O2 -Wall -Wextra -g3 -Wno-sign-compare


clean:
	rm -f ab_tree_test

.PHONY: clean test
