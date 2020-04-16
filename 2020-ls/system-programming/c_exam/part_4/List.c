/*
 * List.c
 *
 *  Created on: 5 abr. 2020
 *      Author: galvez
 */


#include <stdio.h>
#include <stdlib.h>
#include "List.h"

void create(T_List * list) {
	(* list) = NULL;
}

void insert(T_List * list, double value) {
	T_List aux = (T_List)malloc(sizeof(T_Data));
	aux->value = value;
	aux->next = (* list);
	(* list) = aux;
}

void destroy(T_List * list) {
	while((* list) != NULL) {
		T_List aux = (* list)-> next;
		free(* list);
		(* list) = aux;
	}
}
