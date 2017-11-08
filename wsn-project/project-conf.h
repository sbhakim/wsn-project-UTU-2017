

#ifndef __PROJECT_CONF_H__
#define __PROJECT_CONF_H__

/* For RDC driver */

#undef NETSTACK_CONF_RDC
#define NETSTACK_CONF_RDC contikimac_driver


//#define NETSTACK_CONF_RDC  lpp_driver

// #define NETSTACK_CONF_RDC  nullrdc_driver



/* For MAC driver */

#undef NETSTACK_CONF_MAC
#define NETSTACK_CONF_MAC csma_driver

// #define NETSTACK_MAC     nullmac_driver 


#undef NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE
#define NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE 16


 
#endif /* __PROJECT_CONF_H__ */
