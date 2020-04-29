#include <stdio.h>
#include <stdlib.h>
#include "bst.h"

// Create an empty tree
void create(TTree* tree) {
    *tree = NULL;
}

// destroy the tree and free all memory
void destroy(TTree * tree) {
    if (*tree != NULL) {
        destroy(&((*tree)->left));
        destroy(&((*tree)->right));
        free(*tree);
        *tree = NULL;
    }

}

// Insert the value in the tree. If it is already there, do nothing
void insert(TTree* tree, unsigned val) {
    if (*tree == NULL) {
        // insert into empty tree
        *tree = malloc(sizeof(struct TNode));
        (*tree)->val = val;
        (*tree)->left = NULL;
        (*tree)->right = NULL;
    } else if ((*tree)->val == val) {
        // do nothing
    } else if (val < (*tree)->val) {
        // insert val into the left subtree
        insert(&((*tree)->left), val);
    } else {
        // insert val into the right subtree 
        insert(&((*tree)->right), val);
        
    }

}

// Show in screen the contents of the tree, ordered
void show(TTree tree) {
    if(tree != NULL) {
        show(tree->left);
        printf("%d, ", tree->val);
        show(tree->right);
    } 
}

// Save the tree to a file
void save(TTree tree, FILE* f) {
    if(tree != NULL) {
        save(tree->left, f);
        fwrite(&(tree->val), sizeof(tree->val), 1, f);
        save(tree->right, f);
    } 
}

