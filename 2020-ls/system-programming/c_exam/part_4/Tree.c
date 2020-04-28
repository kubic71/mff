#include "Tree.h"
#include "List.h"

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


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


// create a leaf with single double value
T_Tree insertDouble(double value) {
    T_Tree t = calloc(1, sizeof(T_Tree));
    t->discriminant = 'v';
	t->shared.value = value;
	return t;
}


// create a variable leaf node 
T_Tree insertX() {
	T_Tree t = calloc(1, sizeof(T_Tree));
    t->discriminant = 'x';
	return t;
}

T_Tree insertSingle(char discriminant, T_Tree single) {
	// --- sanity check ---
	// allowed unary operations are only:
	//    s, c, r,
	if(isUnaryOp(discriminant)) {
		T_Tree t = calloc(1, sizeof(T_Tree));
    	t->discriminant = discriminant;
		t->shared.single = single;
	} else {
		fprintf(stderr, "Error! %c is not unary operator", discriminant);
		exit(1);		
	}
}

T_Tree insertBoth(char discriminant, T_Tree left, T_Tree right) {
	// --- sanity check ---
	// allowed binary operations are only:
	//    *, /, +, -, p
	if(isBinaryOp(discriminant)) {
		T_Tree t = calloc(1, sizeof(T_Tree));
    	t->discriminant = discriminant;
		t->shared.both.left = left;
		t->shared.both.right = right;
	} else {
		fprintf(stderr, "Error! %c is not binary operator", discriminant);
		exit(1);		
	}
}

bool isUnaryOp(char c) {
	return c == 's' || c == 'c' || c == 'r';
}

bool isBinaryOp(char c) {
	return c == '*' || c == '/' || c == '+' || c == '-' || c == 'p';
}

bool isLeaf(T_Tree t) {
	return t->discriminant == 'x' || t->discriminant == 'v';
}

void destroyTree(T_Tree tree) {
	if(isLeaf(tree)) {
		free(tree);
	} else if(isUnaryOp(tree->discriminant)) {
		destroyTree(tree->shared.single);
		free(tree);

	} else if(isBinaryOp(tree->discriminant)) {
		destroyTree(tree->shared.both.left);
		destroyTree(tree->shared.both.right);
		free(tree);
	} else {
		fprintf(stderr, "Error! destroyTree called with invalid tree data-structure");
		exit(1);
	}
}


// display tree to stdout
void displayTree(T_Tree tree) {
	if(isLeaf(tree)) {
		if(tree->discriminant == 'x') {
			printf("x ");
		} else if(tree->discriminant == 'v')
		{
			printf("%.2lf ", tree->shared.value);
		}

	} else if(isUnaryOp(tree->discriminant)) {
		printf("%c ", tree->discriminant);
		displayTree(tree->shared.single);
	} else if(isBinaryOp(tree->discriminant)) {
		printf("%c ", tree->discriminant);
		displayTree(tree->shared.both.left);
		displayTree(tree->shared.both.right);
	}
}


// Implementation of recursive descent parser for our grammar
// each function corresponds to a grammar rule 
// when function succeeds in parsing, it shifts offset automatically


// shift offset to first non-space character
void skipSpace(char* str, int* offset) {
	while(str[*offset] == ' ') {
		(*offset)++;
	}
}


static char* parseDigits(char* str, int* offset) {
	// number cannot be too large
	int MAX_DIGITS_LEN = 40;

	if(!isdigit(str[*offset])) {
		return NULL;
	}

	char* digits = calloc(MAX_DIGITS_LEN, sizeof(char));
	int i = 0;

	while (isdigit(str[*offset]))
	{
		digits[i] = str[*offset];
		(*offset)++;
		i++;

		if(i >= MAX_DIGITS_LEN/2 - 2){
			fprintf(stderr, "Numbers are too large!");
			exit(1);
		}
	}

	return digits;
}

// return true if parsing is successful
bool parseDouble(char* str, int* offset, double* val) {
	int initial_offset = *offset;

	char* d1 = parseDigits(str, offset);
	if(d1 != NULL) {
		if(str[*offset] == '.') {
			(*offset)++;
			char* d2 = parseDigits(str, offset);
			if(d2 != NULL) {
				strcat(d1, ".");
				strcat(d1, d2);
				sscanf(d1, "%lf", val);

				free(d2);
				free(d1);
				return true;
			}

			free(d1);
			*offset = initial_offset;
			return false;
 		} else {
			sscanf(d1, "%lf", val);
			free(d1);
			return true;
		} 
	} else
	{
		return false;
	}

}

static bool parseSpace(char* str, int* offset) {
	if(str[(*offset)] == ' ') {
		skipSpace(str, offset);
		return true;
	}
	return false;
}

T_Tree parseLeaf(char* str, int* offset) {
	// printf(" parseLeaf: %c\n", str[*offset]);
	int initial_offset = *offset;

	if(str[initial_offset] == 'x') {
		(*offset)++;
		if(parseSpace(str, offset)) {
			return insertX();
		}

		// no space after x
		*offset = initial_offset;
		return NULL;
	} else {
		double val;

		if(parseDouble(str, offset, &val) && parseSpace(str, offset)) {
			return insertDouble(val);
		}

		*offset = initial_offset;
		return NULL;
	}
}


T_Tree parseUnary(char* str, int* offset) {
	// printf("parseUnary %c\n", str[*offset]);
	int initial_offset = *offset;

	char op = str[initial_offset];
	if(isUnaryOp(op)) {
		(*offset)++;
		skipSpace(str, offset);

		T_Tree subtree = parseTree(str, offset);
		if(subtree != NULL) {
			return insertSingle(op, subtree);
		} else {
			// parsing failed, return offset to its original position
			*offset = initial_offset;
			return NULL;
		}
	} else {
		return NULL;
	}
}

T_Tree parseBinary(char* str, int* offset) {
	// printf("parseBinary %c\n", str[*offset]);
	int initial_offset = *offset;

	char op = str[initial_offset];
	if(isBinaryOp(op)) {
		(*offset)++;
		skipSpace(str, offset);

		T_Tree left = parseTree(str, offset);		
		if(left != NULL) {
			T_Tree right = parseTree(str, offset);
			if(right != NULL) {
				return insertBoth(op, left, right);
			} else {
				destroyTree(left);
				*offset = initial_offset;
				return NULL;
			}
		} else {
			// parsing failed, return offset to its original position
			*offset = initial_offset;
			return NULL;
		}
	} else {
		return NULL;
	}
}


// parse tree from string
T_Tree parseTree(char* str, int *offset) {
	// to avoid edge cases, we assume that tree string has additional space at the end

	int initial_offset = *offset;

	skipSpace(str, offset);
	T_Tree t = parseLeaf(str, offset);
	skipSpace(str, offset);
	if(t != NULL)
		return t;

	*offset = initial_offset;
	t = parseUnary(str, offset);
	skipSpace(str, offset);
	if(t != NULL)
		return t;

	*offset = initial_offset;
	t = parseBinary(str, offset);
	skipSpace(str, offset);
	if(t != NULL)
		return t;

	*offset = initial_offset;
	return NULL;

}


static double mult(double x, double y) {
	return x * y;
}

static double divide(double x, double y) {
	if(y == 0) // division by zero
		return NAN;
	return x / y;
}

static double add(double x, double y) {
	return x + y;
}

static double sub(double x, double y) {
	return x - y;
}

T_List evaluateTree(T_Tree tree, double x) {
	if(isBinaryOp(tree->discriminant)) {
		double (*binOp)(double x, double y);

		switch (tree->discriminant)
		{
		case '*':
			binOp = &mult;
			break;

		case '/':
			binOp = &divide;
			break;

		case '+':
			binOp = &add;
			break;

		case '-':
			binOp = &sub;
			break;

		case 'p':
			binOp = &pow;
			break;

		default:
			printf("Error!\n");
			break;
		}

		T_List x_vals = evaluateTree(tree->shared.both.left, x);
		T_List y_vals = evaluateTree(tree->shared.both.right, x);

		T_List results;
		create(&results);

		for(T_List x = x_vals; x != NULL; x = x->next) {
			for(T_List y = y_vals; y != NULL; y = y->next) {
				if(x->value != NAN && y->value != NAN) {
					insert(&results, (*binOp)(x->value, y->value));
				}
			}	
		}

		destroy(&x_vals);
		destroy(&y_vals);
		return results;

	} else if (isUnaryOp(tree->discriminant)) {
		if(tree->discriminant == 'r') {
			T_List vals = evaluateTree(tree->shared.single, x);
			T_List results;
			create(&results);

			for(T_List v = vals; v != NULL; v = v->next) {	
				if(v->value >= 0) {
					insert(&results, sqrt(v->value));
					insert(&results, -sqrt(v->value));
				}
				
			}	

			destroy(&vals);
			return results;
		} else
		{
			double (*unOp)(double x);

			switch (tree->discriminant)
			{
			case 's':
				unOp = &sin;
				break;

			case 'c':
				unOp = &cos;
				break;

			}

			T_List vals = evaluateTree(tree->shared.single, x);
			for(T_List v = vals; v != NULL; v = v->next) {	
				v->value = (*unOp)(v->value);
			}	

			return vals;
		}		
	} else if (tree->discriminant == 'x') {
		T_List l;
		create(&l);
		insert(&l, x);
		return l;
	} else if (tree->discriminant == 'v') {
		T_List l;
		create(&l);
		insert(&l, tree->shared.value);
		return l;
	} else {
		fprintf(stderr, "Error in expression tree evaluation, no case matched for: %c", tree->discriminant);
		exit(1);
	}
}