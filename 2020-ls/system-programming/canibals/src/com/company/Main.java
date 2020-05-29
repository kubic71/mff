package com.company;

public class Main {

    public static void main(String[] args) {
	// write your code here
       int num_can = 5;
       Pot pot = new Pot();
       Cook cook = new Cook(pot);
       cook.start();

       for(int i = 0; i < num_can; i++ ) {
           Canibal c = new Canibal(pot);
           c.start();
       }
    }
}
