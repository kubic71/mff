package com.company;

import java.util.concurrent.Semaphore;

public class Pot {
    int readyMeals = 0;
    public static  final int COOKED_AT_ONCE = 3;

    private Semaphore mutex = new Semaphore(1, true);
    private Semaphore waitForWakeup = new Semaphore(0, true);
    private Semaphore waitForNewMeal = new Semaphore(0,true);

    public void eat() throws InterruptedException {
       mutex.acquire();

       if (readyMeals == 0) {
           // wakeup cook and wait for his new meal
           System.out.println("Not enouch meals, waking up cook!");
          waitForWakeup.release();

          waitForNewMeal.acquire();
          System.out.printf("Cook made new meals, now we have %d meals available\n", readyMeals);
       }

       readyMeals--;
       System.out.println("Canibal ate a meal");

       mutex.release();
    }

    public  void cook() throws InterruptedException {
        // someone woke us up and is waiting for his meal, because the bowl is empty
        waitForWakeup.acquire();
        System.out.printf("I am the cook and I am making you %d new meals\n", COOKED_AT_ONCE);
        readyMeals += COOKED_AT_ONCE;
        waitForNewMeal.release();
    }

}
