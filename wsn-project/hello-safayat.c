#include "contiki.h"
#include "powertrace.h"

#include <stdio.h>

/*----------------------------------------------*/
PROCESS (hello_world_process, "Hello World Process");
AUTOSTART_PROCESSES (&hello_world_process);

/*----------------------------------------------*/

PROCESS_THREAD(hello_world_process, ev, data)
{
	PROCESS_BEGIN();
	powertrace_start(CLOCK_SECOND * 2);
	
	printf ("Hello, Safayat !! \n");
	
	
	PROCESS_END();	
}
/*-----------------------------------------------*/
