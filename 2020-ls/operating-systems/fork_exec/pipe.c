/* 
 * File:   simple_spawn_0.c
 * Author: Guillermo Pérez Trabado <guille@ac.uma.es>
 *
 * Created on 24 de abril de 2017, 14:39
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char **argv)
{

    int status;
    pid_t pid;
    int code;
    int signum;

    int p[2];
    if (pipe(p) < 0)
    {
        printf("Pipe couldn't be created\n");
        exit(1);
    }

    // execute producer
    pid = fork();
    if (pid == 0)
    {
        printf("Excuting cut -c1-4, pid=%d\n", getpid());

        // redirect stdout to the pipe
        dup2(p[1], 1);
        char *exec_args[] = {"cut", "-c1-4", NULL};
        execvp("cut", exec_args);

        fprintf(stderr, "child: error in exec\n");
        fprintf(stderr, "errno: %d\n", errno);

        exit(EXIT_FAILURE);
    }

    // close the write end of the pipe in parent
    // if we didn't do that, after 'cut' would finish its execution, the EOF wouldn't be sent to pipe,
    // because it would still be open in the parent process
    close(p[1]);

    // execute the consumer
    pid = fork();

    if (pid == 0)
    {
        // redirect pipe to stdin
        dup2(p[0], 0);
        char *exec_args[] = {"nl", NULL};
        execvp("nl", exec_args);

        fprintf(stderr, "child: error in exec\n");
        fprintf(stderr, "errno: %d\n", errno);

        exit(EXIT_FAILURE);
    }

    fprintf(stderr, "parent: waiting for children\n", getpid());

    while ((pid = waitpid(-1, &status, WUNTRACED | WCONTINUED)) != -1)
    {
        // Status is a multifield value with this information:
        //      Event: Type of state change (EXITED|TERMINATED BY SIGNAL|STOPPED|CONTINUED)
        //      Event information: Number of the signal which terminated/stopped the child
        //      Exit code for exited processes.

        // Use macros to check fields. NEVER USE status directly!!!
        if (WIFEXITED(status))
        {
            code = WEXITSTATUS(status);
            fprintf(stderr, "parent: child %d terminated with exit(%d)\n", pid, code);
        }
        if (WIFSIGNALED(status))
        {
            signum = WTERMSIG(status);
            fprintf(stderr, "parent: child %d kill by signal %d\n", pid, signum);
        }
        if (WIFSTOPPED(status))
        {
            signum = WSTOPSIG(status);
            fprintf(stderr, "parent: child %d stopped by signal %d\n", pid, signum);
        }
        if (WIFCONTINUED(status))
        {
            fprintf(stderr, "parent: child %d continued\n", pid);
        }
    }

    /* Only parent process should reach here */
    return (EXIT_SUCCESS);
}
