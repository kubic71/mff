package com.company;

import static java.lang.Thread.sleep;

import java.util.Random;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/*
 * Name: Jakub
 * Surname: Hejhal
 */

public class Bus {
    private Random r = new Random();
    private int currentlyOnboard = 0;


    private int numCritical = Driver.NUM_CRITICAL;
    private int numMinor = Driver.NUM_MINOR;
    private int numUnharmed = Driver.NUM_UNHARMED;


    ReentrantLock lock = new ReentrantLock(true);
    Condition criticalCond = lock.newCondition();
    Condition minorCond = lock.newCondition();
    Condition unharmedCond = lock.newCondition();

    Condition ambulanceFull = lock.newCondition();

    boolean canBoard = false;
    Condition canBoardCond = lock.newCondition();

    public void waitDisinfection() {
        try {
            sleep(r.nextInt(2000));
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }

    public void onBoardAmbulance(PassengerType type) {

        lock.lock();
        try {
            // stand in the priority queue
            if (type == PassengerType.UNHARMED) {
                while (numCritical > 0 || numMinor > 0) {   // wait for all harmed to be boarded
                    unharmedCond.await();
                }
            } else if (type == PassengerType.MINOR) {
                while (numCritical > 0) {    // wait for all Critical to be boarded
                    minorCond.await();
                }
            } else if (type == PassengerType.CRITICAL) {
                // don't wait for anybody
            }


            // board only if the ambulance is available
            // canBoard == true iif ambulance is available and has at least one free space
            while (!canBoard) {
                canBoardCond.await();
            }

            // board the ambulance till it's full
            if (type == PassengerType.UNHARMED) {
                numUnharmed--;
            } else if (type == PassengerType.MINOR) {
                numMinor--;
                if (numMinor == 0) {
                    unharmedCond.signalAll();
                }

            } else if (type == PassengerType.CRITICAL) {
                numCritical--;
                if (numCritical == 0) {
                    minorCond.signalAll();
                }
            }

            currentlyOnboard++;

            if (currentlyOnboard == Driver.CAPACITY) {
                canBoard = false;
                ambulanceFull.signal();
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public void performTrip(int cap) {
        lock.lock();
        try {
            currentlyOnboard = 0;

            canBoard = true;
            canBoardCond.signalAll();

            // In general case, we would also have to check, that there are no people left at the site, but we know that the total number of people is divisible by ambulance capacity
            // so we don't have to
            while (currentlyOnboard < cap) {
                try {
                    ambulanceFull.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } catch ( Exception e ) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }

    }
}
