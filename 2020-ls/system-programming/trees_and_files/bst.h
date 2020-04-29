#ifndef BST_H_
#define BST_H_
#include <stdio.h>

typedef struct TNode* TTree;

	struct TNode {
			unsigned val;
			TTree left, right;
		};

// Create an empty tree
void create(TTree* tree);

// destroy the tree and free all memory
void destroy(TTree * tree);

// Insert the value in the tree. If it is already there, do nothing
void insert(TTree* tree,unsigned val);

// Show in screen the contents of the tree, ordered
void show(TTree tree);

// Save the tree to a file
void save(TTree tree, FILE* f);


#endif /* BST_H_ */
