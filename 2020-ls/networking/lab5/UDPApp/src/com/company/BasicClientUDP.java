package com.company;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class BasicClientUDP {
    String serverIp;
    int serverPort;

    DatagramSocket socket;

    BasicClientUDP(String serverIp, int serverPort) {
        this.serverIp = serverIp;
        this.serverPort = serverPort;
    }


    public void send(String response) throws IOException, UnknownHostException {
        byte[] buf = response.getBytes();
        DatagramPacket packet = new DatagramPacket(buf, buf.length);
        socket.send(packet);
    }

    public String receive() throws IOException {
        byte[] receive = new byte[BasicServerUDP.BUFFER_LEN];
        DatagramPacket packet = new DatagramPacket(receive, receive.length);
        socket.receive(packet);

        return Util.bufferToString(receive);
    }

    public void start() throws IOException {
        Scanner scanner = new Scanner(System.in);

        socket = new DatagramSocket();
        System.out.println("Connecting to server...");

        // Client will be able send and receive datagrams to/from server socket addr
        try {
            socket.connect(InetAddress.getByName(serverIp), serverPort);
            socket.setSoTimeout(5000);
        } catch (Exception e) {
            System.out.println("Couldn't connect to the server...");
            System.exit(1);
        }

        try {
            while (true) {
                String msg = "";
                System.out.print("Command: ");
                String command = scanner.nextLine();
                msg += command + "\r\n";

                if (command.equals("F")) {
                    System.out.println("Exiting UDP client.");
                    return;
                }

                System.out.print("Content: ");
                msg += scanner.nextLine();

                System.out.println("Sending datagram to server...");
                send(msg);

                System.out.println("Waiting for server response...");
                try {
                    System.out.println(receive());
                } catch (SocketTimeoutException e) {
                    System.out.println("Request timed out.");
                    continue;
                }


            }
        } catch (Exception e) {
            System.out.println("Connection broken!");
        }
    }
}
