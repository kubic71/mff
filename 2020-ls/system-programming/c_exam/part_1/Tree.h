/*
 * Tree.h
 *
 *  Created on: 5 abr. 2020
 *      Author: galvez
 */

#ifndef TREE_H_
#define TREE_H_

#include <stdbool.h>
typedef struct _Node * T_Tree;

typedef struct _Node {
	// Valid values of discriminant are:
	// * Multiply
	// / Divide
	// + Add
	// - Subtract
	// v Double literal constant
	// x Variable
	// r Square root
	// s Sine
	// c Cosine
	// p Power
	char discriminant;
	union {
		struct {
			T_Tree left;
			T_Tree right;
		} both;
		T_Tree single;
		double value;
	} shared;
} T_Node;

T_Tree insertDouble(double value);
T_Tree insertX();
T_Tree insertSingle(char discriminant, T_Tree single);
T_Tree insertBoth(char discriminant, T_Tree left, T_Tree right);

bool isLeaf(T_Tree t);
bool isUnaryOp(char c);
bool isBinaryOp(char c);


void destroyTree(T_Tree tree);
void displayTree(T_Tree tree);
double evaluateTree(T_Tree tree, double x);


void skipSpace(char* str, int* offset);
bool parseDouble(char* str, int* offset, double* val);
T_Tree parseLeaf(char* str, int* offset);
T_Tree parseUnary(char* str, int* offset);
T_Tree parseBinary(char* str, int* offset);
T_Tree parseTree(char* str, int* offset);

#endif /* TREE_H_ */
