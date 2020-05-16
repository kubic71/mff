package com.company;

import java.io.*;
import java.net.*;
import java.util.*;

public class BasicServerTCP {
    PrintWriter outS;
    BufferedReader recvS;
    Socket clientSocket;
    ServerSocket server;
    int serverPort;

    public BasicServerTCP(int serverPort) {
        this.serverPort = serverPort;

    }

    public void start() {
        System.out.println("Starting server at 0.0.0.0:" + Integer.toString(serverPort));
        try {
            bindServer();
        }  catch (IOException e) {
           System.out.println("Cannot bind to 0.0.0.0.:" + Integer.toString(serverPort));
           return;
        }

        while (true) {
           serveClient();
        }
    }

    private void bindServer() throws IOException {
        server = new ServerSocket(serverPort, 1);
    }


    private void serveClient() {
        // Serving client until either client closes connection or exception is raised
        try {

            System.out.println("Waiting for a connection");
            clientSocket = server.accept();
            System.out.println("Incoming connection from " + clientSocket.getInetAddress().toString() + ":" + clientSocket.getPort());




            recvS = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            outS = new PrintWriter(clientSocket.getOutputStream(), true);

            outS.println("Welcome to the text transformation service");

            while (true) {
                // handle one command in each iteration

                String command = recvS.readLine();
                if (command.equals("F")) {
                    System.out.println("Closing the connection");
                    outS.println("OK");
                    clientSocket.close();
                    return;
                }

                String content = recvS.readLine();

                if (command.equals("L")) {
                    System.out.println("Serving L command");
                    outS.println(removeExtraWhiteCharacters(content));

                } else if (command.equals("B")) {
                    System.out.println("Serving B command");
                    content = removeExtraWhiteCharacters(content);

                    // shuffle the words
                    String[] words = content.split(" ");
                    List<String> wordsList = Arrays.asList(words);
                    Collections.shuffle(wordsList);

                    outS.println(String.join(" ", wordsList));

                } else {
                    outS.println("Not supported option");
                    System.out.println("Not supported command: " + command);
                }

            }
        } catch (Exception e) {
            closeConnection();
            System.out.println("Connection closed");
            // when the client closes the connection abruptly, exception is catched here
        }
    }


    private void closeConnection() {
        try
        {
            clientSocket.close();
        } catch (Exception ignored) {
        }
    }

    private String removeExtraWhiteCharacters(String content) {
        content = content.replaceAll("\\s+", " ");
        return content.strip();
    }

}

