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

#define MAX_ARGS 256

/* Executes program, redirecting stdin and stdout from and to file given by the last two cmd params
 * argv[1] - command to execute
 * argv[2, 3, 4, ...] - command params
 * argv[-2] - file for stdin redirection
 * argv[-1] - file for stdout redirection
 * 
 * For example:
 * std_recirect head -n5 /etc/passwd first_five_users.txt
 * will execute 'head' cmd with '-n5' parameter, reading from /etc/passwd and outputting to first_five_users.txt file
 */
int main(int argc, char** argv)
{
    int status;
    pid_t pid;
    int code;
    int signum;
    char* executable_args[MAX_ARGS];

    pid = fork();
    if (pid == -1)
    {
        /* Error in fork: This is severe!!! Abort further processing!!! */
        fprintf(stderr, "parent: error in fork\n");
        exit(EXIT_FAILURE);
    }

    if (pid == 0)
    {
        
        // copy executable args 

        printf("Executing %s with args:", argv[1]);
        for(int i = 1; i < argc - 2; i++) {
            executable_args[i - 1] = argv[i];
            printf("%s ", executable_args[i - 1]);
        }
        printf("\n");
        executable_args[argc - 3] = NULL;

        // We do not need to manually close fd 0 and 1, because dup2(int oldfd, int newfd) atomically closes newfd, if used and duplicates oldfd
        // From man 2 dup: ...If the  file  descriptor  newfd  was  previously open, it is silently closed before being reused.
        // The  steps  of  closing  and  reusing  the file descriptor newfd are performed atomically.  This is important, 
        // because trying to implement equivalent functionality using close(2) and dup() would be subject to race conditions,
        // whereby newfd might be reused between the two steps.  Such reuse could happen because the main program is interrupted by a
        //  signal handler that allocates a file descriptor, or because a parallel thread  allocates  a  file  de?scriptor.

        // redirect file to stdin
        printf("Redirecting %s to stdin\n", argv[argc-2]);
        int f_in=open(argv[argc - 2],O_RDONLY);
        dup2(f_in,0);
        

        // redirect stdout to file

        printf("Redirecting stdout to %s\n", argv[argc-1]);
        int f_out = open(argv[argc-1], O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
        dup2(f_out,1);

        execvp(argv[1], executable_args);

        
        /* Error in exec: This is severe!!! Abort further processing in child!!!
         * Notify parent process through exit code!!!
         * Assign special return values to each kind of error.
         */
        fprintf(stderr, "child: error in exec\n");
        fprintf(stderr, "errno: %d\n", errno);
        close(f_in);
        close(f_out);

        exit(EXIT_FAILURE);
    }
    else
    {
        /***************************************************************************/
        /* This is the parent process after fork. Evey change in this section
         * only affects the parent environment.
         */

        // <POST-FORK PARENT ONLY CODE HERE>
        fprintf(stderr, "parent: waiting for children\n", getpid());

        //  Usual parent tasks are controlling the life of children after creation:
        //      Wait for children to end and notifying somebody about status.
        //      Killing children before parent's exit in order to leave system in a clean state.
        //      Stop and continue children in order to be smart with CPU and RAM resources.
        //      Change children priority dynamically to allow smarter scheduling of CPU.

        // This call notifies not only termination but also state changes from children
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
        /***************************************************************************/
    }

    /* Only parent process should reach here */
    return (EXIT_SUCCESS);
}

