/* 
 * File:   simple_signal_1.c
 * Author: Guillermo P�rez Trabado <guille@ac.uma.es>
 *
 * Created on 24 de abril de 2017, 14:39
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>
#define MAX_ARGS 256
#define MAX_MESSAGE 2048

/* reverse:  reverse string s in place */
void reverse(char s[])
{
    int i, j;
    char c;

    for (i = 0, j = strlen(s) - 1; i < j; i++, j--)
    {
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

/* itoa:  convert n to characters in s */
void itoa(int n, char s[])
{
    int i, sign;

    if ((sign = n) < 0) /* record sign */
        n = -n; /* make n positive */
    i = 0;
    do
    { /* generate digits in reverse order */
        s[i++] = n % 10 + '0'; /* get next digit */
    }
    while ((n /= 10) > 0); /* delete it */
    if (sign < 0)
        s[i++] = '-';
    s[i] = '\0';
    reverse(s);
}

/**
 * Actions to be executed when a child has changed its state
 * @param sig
 * @return 
 */
void signal_handler(int sig)
{
    int status;
    pid_t pid;
    int code;
    int signum;
    char message[MAX_MESSAGE + 1];

    // We are inside an interrupt handler:
    //      DO NOT LOOP/BLOCK WAITING FOR EVENTS!!!
    //      DO NOT USE UNSAFE NON-REENTRANT FUNCTIONS!!!
    //      See "man 2 signal" for the POSIX 1003.1 list of safe functions.

    // printf is not safe in signals. Use write. Format message using basic & safe
    // formatting functions. Sorry: sprintf is not safe!!!
    strncpy(message, "parent: SIGCHLD received\n", MAX_MESSAGE);
    write(2, message, strlen(message));

    // Loop until all pending status changes have been received with waitpid.
    // But never BLOCK or iterate forever ==> USE WNOHANG!!!
    while ((pid = waitpid(-1, &status, WUNTRACED | WCONTINUED | WNOHANG)) > 0)
    {
        if (WIFEXITED(status))
        {
            code = WEXITSTATUS(status);
            strncpy(message, "parent: child ", MAX_MESSAGE);
            itoa(pid,&message[strlen(message)]);
            strncat(message, " terminated with exit(", MAX_MESSAGE - strlen(message));
            itoa(code,&message[strlen(message)]);
            strncat(message, ")\n", MAX_MESSAGE - strlen(message));
            write(2, message, strlen(message));
        }
        if (WIFSIGNALED(status))
        {
            signum = WTERMSIG(status);
            strncpy(message, "parent: child ", MAX_MESSAGE);
            itoa(pid,&message[strlen(message)]);
            strncat(message, " killed by signal ", MAX_MESSAGE - strlen(message));
            itoa(signum,&message[strlen(message)]);
            strncat(message, "\n", MAX_MESSAGE - strlen(message));
            write(2, message, strlen(message));
        }
        if (WIFSTOPPED(status))
        {
            signum = WSTOPSIG(status);
            strncpy(message, "parent: child ", MAX_MESSAGE);
            itoa(pid,&message[strlen(message)]);
            strncat(message, " stopped by signal ", MAX_MESSAGE - strlen(message));
            itoa(signum,&message[strlen(message)]);
            strncat(message, "\n", MAX_MESSAGE - strlen(message));
            write(2, message, strlen(message));
        }
        if (WIFCONTINUED(status))
        {
            fprintf(stderr, "parent: child %d continued\n", pid);
            strncpy(message, "parent: child ", MAX_MESSAGE);
            itoa(pid,&message[strlen(message)]);
            strncat(message, " continued\n", MAX_MESSAGE - strlen(message));
            write(2, message, strlen(message));
        }
    }
}

/*
 * 
 */
int main(int argc, char** argv)
{
    pid_t pid;
    int pipefd[2];

    char *executable_file;
    char *executable_args[MAX_ARGS];

    // Program handler for SIGCHLD before any children is created
    signal(SIGCHLD, signal_handler);


    /***************************************************************************/
    /* <PIPES NEED TO BE INHERITED FROM PARENT>
     * CREATE an unamed pipe for communication between processes
     */
    pipe(pipefd);
    /***************************************************************************/

    // Create first process
    pid = fork();

    /* Errors in fork mean that there is no child process. Parent is alone. */
    if (pid == -1)
    {
        fprintf(stderr, "parent: error in fork\n");
        exit(1);
    }

    if (pid == 0)
    {
        /***************************************************************************/
        /* This is the first child process. Evey change in this section only affects the
         * child environment.
         */

        // <POST-FORK CHILD ONLY CODE HERE>

        // Redirect stdout to pipefd[1]
        // Close inherited standard output file descriptor
        close(1);
        // Copy writing pipe descriptor on stdout
        dup2(pipefd[1], 1);
        // Close all pipe descriptors to avoid having unknown duplicates
        close(pipefd[1]);
        close(pipefd[0]);

        executable_file = "/bin/cat";
        executable_args[0] = "mypipecat"; // A custom name for the process
        executable_args[1] = NULL; // Last argument

        fprintf(stderr, "child 1: %d %s\n", getpid(), executable_file);
        execvp(executable_file, executable_args);

        fprintf(stderr, "child: error in exec\n");
        //        exit(EXIT_FAILURE);
    }
    else
    {
        // Create second process
        pid = fork();

        /* Errors in fork mean that there is no child process. Parent is alone. */
        if (pid == -1)
        {
            fprintf(stderr, "parent: error in second fork\n");
            exit(EXIT_FAILURE);
        }

        if (pid == 0)
        {
            /***************************************************************************/
            /* This is the second child process. Evey change in this section only affects the
             * child environment.
             */

            // <POST-FORK CHILD ONLY CODE HERE>

            // Redirect stdin from pipefd[0]
            // Close inherited standard output file descriptor
            close(0);
            // Copy reading pipe descriptor on stdin
            dup2(pipefd[0], 0);
            // Close all pipe descriptors to avoid having unknown duplicates
            close(pipefd[1]);
            close(pipefd[0]);

            executable_file = "/usr/bin/nl";
            executable_args[0] = "mypipenl"; // A custom name for the process
            executable_args[1] = NULL; // Last argument

            fprintf(stderr, "child 2: %d %s\n", getpid(), executable_file);
            execvp(executable_file, executable_args);

            fprintf(stderr, "child 2: error in exec\n");
            exit(EXIT_FAILURE);
        }
        else
        {
            // <POST-FORK PARENT ONLY CODE HERE>

            int next_drink;

            // <PARENT MUST CLOSE DESCRIPTORS FROM PIPES IN USE BY CHILDREN>
            close(pipefd[1]);
            close(pipefd[0]);

            // We just do some work every 10 seconds
            next_drink = 10;
            while (1)
            {
                int time_left = sleep(next_drink);
                if (time_left > 0)
                {
                    printf("We were waken up before time. Wait %d seconds left.\n", time_left);
                    next_drink = time_left;
                }
                else
                {
                    printf("Time to go to the fridge and get a drink!\n");
                    next_drink = 10;
                }
            }
        }

        /* Only parent process should reach here */
        return (EXIT_SUCCESS);
    }
}


