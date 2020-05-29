package com.company;

import static java.lang.Thread.onSpinWait;
import static java.lang.Thread.sleep;

import java.util.Random;
import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/*
 * Name: Jakub
 * Surname: Hejhal
 */

public class BusSemaphores {
    private Random r = new Random();
    private volatile int alreadyTaken = 0;


    private Semaphore passengerMutex = new Semaphore(1, true);
    private Ticket[] tickets = new Ticket[50];


    public BusSemaphores() {
        for (int i = 0; i < 50; i++) {
            tickets[i] = new Ticket();
        }
    }


    public void waitDisinfection() {
        try {
            sleep(r.nextInt(2000));
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }

    public void onBoardAmbulance(PassengerType type, int passengerID) {
        try {
            passengerMutex.acquire();

            int index = 0;
            // stand in the priority queue
            if (type == PassengerType.UNHARMED) {
                index = Driver.NUM_CRITICAL + Driver.NUM_MINOR;
            } else if (type == PassengerType.MINOR) {
                index = Driver.NUM_CRITICAL;
            } else if (type == PassengerType.CRITICAL) {
                index = 0;
            }

            while (!tickets[index].placeFree) {
                index++;
            }

            // reserve place in the queue
            tickets[index].placeFree = false;
            passengerMutex.release();

            tickets[index].waitForAmbulance.acquire();

            System.out.println(type + " " + passengerID + " is inside the ambulance.");
            // when ambulance calls me in, I acknowledge
            tickets[index].ackAmbulance.release();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void performTrip(int cap) {
        try {
            for (int i = alreadyTaken; i < cap + alreadyTaken; i++) {

                // tell passenger he can board
                tickets[i].waitForAmbulance.release();

                // wait for him to board
                tickets[i].ackAmbulance.acquire();
            }

            alreadyTaken += cap;


        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
