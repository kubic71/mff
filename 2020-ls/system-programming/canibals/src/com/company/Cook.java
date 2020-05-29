package com.company;

public class Cook extends  Thread {
    Pot pot;

    public Cook(Pot pot) {
        this.pot = pot;
    }
    @Override
    public void run() {
        while (true) {
            try {
                pot.cook();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
