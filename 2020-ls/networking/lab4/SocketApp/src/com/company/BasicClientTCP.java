package com.company;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class BasicClientTCP {
    String serverIp;
    int serverPort;


    PrintWriter outS;
    BufferedReader recvS;

    Socket socket;

    BasicClientTCP(String serverIp, int serverPort) {
        this.serverIp = serverIp;
        this.serverPort = serverPort;
    }


    public void start() throws IOException {
        Scanner scanner = null;
        try {
            socket = new Socket(serverIp, serverPort);
            System.out.printf("Connected to %s:%d\n", serverIp, serverPort);

            outS = new PrintWriter(socket.getOutputStream(), true);
            recvS = new BufferedReader(new InputStreamReader(socket.getInputStream()));


            // Print the welcome message
            System.out.println(recvS.readLine());
            scanner = new Scanner(System.in);
        } catch (Exception e) {
            System.err.printf("Cannot connect to %s:%d", serverIp, serverPort);
            System.exit(1);
        }

        try {
            while (true) {

                System.out.print("Command: ");

                String command = scanner.nextLine();
                outS.print(command + "\r\n");
                outS.flush();

                if (command.equals("F")) {
                    System.out.println("Closing connection");
                    String ok = recvS.readLine();
                    System.out.println("Server: " + ok);

                    closeSocket();
                    return;
                }

                System.out.print("Content: ");
                outS.println(scanner.nextLine());

                System.out.println("Waiting for response...");
                System.out.println(recvS.readLine());

            }
        } catch (Exception e) {
            System.out.println("Connection closed");
        }
    }

    private void closeSocket() {
        try {
            socket.close();
        } catch (Exception ignored) {
        }
    }


}
