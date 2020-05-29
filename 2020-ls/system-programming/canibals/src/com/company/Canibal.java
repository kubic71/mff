package com.company;

public class Canibal extends Thread {
    private Pot pot;

    Canibal(Pot pot) {
        this.pot = pot;
    }


    @Override
    public void run() {
        while (true) {
            try {
                pot.eat();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
